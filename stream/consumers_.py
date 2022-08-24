from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from threading import Condition

class Frame(object):
    condition = Condition()
    content = bytes()

theFrame = Frame()

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_name = self.scope['url_route']['kwargs']['device_name']
        await self.channel_layer.group_add(self.device_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, code):
        print ('Disconnect')
        #return super().disconnect(code)
        await self.channel_layer.group_discard(self.device_name, self.channel_name)
        
    async def receive(self, text_data=None, bytes_data=None):
        frame = bytes_data
        #print (f'Receive: Text: {type(text_data)} Bytes: {len(bytes_data)}')
        # Send it to the group
        await self.channel_layer.group_send(self.device_name,
            {'type': 'send_frame', 'message' : frame, 'sender' : self.channel_name}
            )
            #{'type': 'send_frame'}
            #)
        # frame = bytes_data
        # #print (f'Receive: Text: {type(text_data)} Bytes: {len(bytes_data)}')
        # with theFrame.condition:
        #     theFrame.content = frame
        #     print ('saved to frame')
        #     theFrame.condition.notify_all()

        # # Send it to the group
        # await self.channel_layer.group_send(
        #     self.device_name,
        #     # {'type': 'send_frame', 'message' : frame}
        #     # )
        #     {'type': 'send_frame'}
        #     )
        # await self.channel_layer.send(
        #     'client',
        #     {'type': 'send_frame'}
        #     )
        # await self.channel_layer.flush()

    async def send_frame(self, event):
        if event['sender'] != self.channel_name:
            print ('send')
            frame = event['message']
            await self.send(bytes_data = frame)
        else:
            pass

    # async def send_frame(self, *args):
    #         print ('send_frame_ex')
    #         while True:
    #             with theFrame.condition:
    #                 print ('waiting for frame')
    #                 theFrame.condition.wait()
    #                 await self.send(bytes_data = theFrame.content)

class ClientStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Connection request by client')
        self.channel_name = 'client'
        await self.accept()
        while True:
            with theFrame.condition:
                print ('waiting for frame')
                theFrame.condition.wait()
                await self.send(bytes_data = theFrame.content)
    
    async def disconnect(self, code):
        print ('Disconnect')
        
    # async def send_frame(self, event):
    #     frame = event['message']
    #     print ('sending')
    #     await self.send(bytes_data = frame)

    async def send_frame(self):
        print ('send_frame_ex')
        while True:
            with theFrame.condition:
                print ('waiting for frame')
                theFrame.condition.wait()
                await self.send(bytes_data = theFrame.content)