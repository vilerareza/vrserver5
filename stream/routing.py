from django.urls import re_path
from django.urls import path

from .consumers import DeviceFrameConsumer, DeviceControlConsumer, ClientConsumer

websocket_urlpatterns = [
    re_path('ws/frame/(?P<device_name>\w+)/$', DeviceFrameConsumer.as_asgi()),
    re_path('ws/control/(?P<device_name>\w+)/$', DeviceControlConsumer.as_asgi()),
    re_path('client/(?P<device_name>\w+)/$', ClientConsumer.as_asgi())
    ]