
from django.http import JsonResponse
from .consumers import frames

# Create your views here.
def get_stream_status(request, device_name):
    stream = False
    if device_name in frames:
        stream = True
    statusResponse = JsonResponse({'stream': stream})
    return statusResponse