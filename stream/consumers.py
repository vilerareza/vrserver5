from channels.generic.websocket import WebsocketConsumer
from threading import Thread
import json
from functools import partial
from .streamobject import Frame, Control
import ai_manager

deviceFrameConsumers = {}
deviceControlConsumers = {}
frames = {}
#controls = {}
aiManager = ai_manager.aiManager

class DeviceFrameConsumer(WebsocketConsumer):
    stop_flag = False
    processThisFrame = True
    t_process_frame = Thread()

    def connect(self):
        print ('Device frame connected')
        self.device_name = self.scope['url_route']['kwargs']['device_name']
        try:
            # Subscribe
            self.frame = frames[self.device_name]
            #self.control = controls[self.device_name]
        except:
            # Register self to consumers dict
            deviceFrameConsumers[self.device_name] = self
            # Create frame object and register to frames dict
            self.frame = Frame()
            frames[self.device_name] = self.frame
            # Create control object and register to controls dict
            #self.control = Control()
            #controls[self.device_name] = self.control

        self.accept()
        self.start_monitor_stream()
    
    def disconnect(self, code):
        super().disconnect(code)
        self.stop_flag = True
        self.close()
        print ('Device disconnected')
        
    def receive(self, text_data=None, bytes_data=None):
        # Receive frame bytes data from camera
        #print (f'Receive: Text: {type(text_data)} Bytes: {len(bytes_data)}')
        #self.frame.content = bytes_data
        #self.frame.condition.notify_all()
        if not self.t_process_frame.is_alive():
            self.t_process_frame = Thread(target = partial(self.start_process_frame, bytes_data))
            self.t_process_frame.daemon = True
            self.t_process_frame.start()
        # else:
        #     print ('bypass')

    def start_monitor_stream(self):
        # Monitor the stream adtivity from device
        # Declare timeout and pop the self.frame object from frames dict
        def monitor_stream():
            while not self.stop_flag:
                try:
                    with self.frame.condition:
                        if not (self.frame.condition.wait(timeout = 10)):
                            print ('timeout')
                            frames.pop(self.device_name)
                            deviceFrameConsumers.pop(self.device_name)
                            deviceControlConsumers.pop(self.device_name)
                except Exception as e:
                    print (e)
        Thread(target=monitor_stream).start()

    def start_process_frame(self, bytes_data):
        # '''Detect and extraction'''
        #img_bytes = aiManager.bound_faces(detector_type = 1, bytes_data = bytes_data)
        img_bytes = aiManager.recognize(detector_type = 1, bytes_data = bytes_data)
        # if len(bboxes) > 0:
        #     print ('face detected')
        with self.frame.condition:
            self.frame.content = img_bytes
            self.frame.condition.notify_all()

class DeviceControlConsumer(WebsocketConsumer):

    def connect(self):
        print ('Device control socket connected')
        self.device_name = self.scope['url_route']['kwargs']['device_name']
        # Register self to device control consumers dict
        deviceControlConsumers[self.device_name] = self
        self.accept()
    
    def disconnect(self, code):
        super().disconnect(code)
        self.close()
        print ('Device control socket disconnected')


class ClientConsumer(WebsocketConsumer):
    stop_flag = False

    def connect(self):
        print ('Client connected')
        self.device_name = self.scope['url_route']['kwargs']['device_name']
        
        try:
            # Subscribe
            self.frame = frames[self.device_name]
            #self.control = controls[self.device_name]
            self.accept()
            Thread(target=self.send_frame).start()
            #self.t1 = Thread(target=self.send_frame)
            #self.t1.daemon = True
            #self.t1.start()
        except:
            self.close()
        #     self.frame = Frame()
        #     frames[self.device_name] = self.frame
    
    def disconnect(self, code):
        try:
            super().disconnect(code)
            self.stop_flag = True
            self.t1.join()
            self.close()
            print ('Client disconnected')
        except:
            pass
            # It is possible to close the connection at connect. So ignore the exception.

    def send_frame(self):
        while not self.stop_flag:
            #print ('send frame function')
            try:
                with self.frame.condition:
                    if (self.frame.condition.wait(timeout = 3)):
                        self.send(bytes_data = self.frame.content)
                    else:
                        print ('timeout')
            except Exception as e:
                print (e)

    def receive(self, text_data=None):
        control = json.loads(text_data)
        print (control)
        try:
            deviceControlConsumers[self.device_name].send(text_data)
        except Exception as e:
            print (e)
        # with self.control.condition:
        #     self.control.command = json.loads(text_data)
        #     print (self.control.command)
        #     deviceConsumers[self.device_name] = self.control.command
        #     self.control.condition.notify_all()