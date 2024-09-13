from django.urls import path
from .views import camera_capture, upload_image

urlpatterns = [
    path('api/upload/', upload_image, name='upload_image'), 
    path('api/images/', camera_capture, name='camera_capture'),
]
