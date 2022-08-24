from django.urls import path
from . import views

urlpatterns = [
    path('status/<str:device_name>/', views.get_stream_status),
]