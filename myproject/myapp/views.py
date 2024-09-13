import os
import base64
import logging
from django.core.files.base import ContentFile
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CapturedImage
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

# Ensure that the directory exists
def ensure_media_directory_exists():
    media_root = settings.MEDIA_ROOT
    target_dir = os.path.join(media_root, 'captured_images')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

# View to render the camera page
def camera_capture(request):
    return render(request, 'capture.html')

# API view to handle image upload
@api_view(['POST'])
def upload_image(request):
    image_data = request.data.get('image_data')

    if not image_data:
        return Response({'error': 'No image data provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Ensure that the directory exists
        ensure_media_directory_exists()

        # Decode the base64 image data
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        image = ContentFile(base64.b64decode(imgstr), name=f"upload.{ext}")

        # Save the image to the database (CapturedImage model)
        captured_image = CapturedImage.objects.create(image=image)

        # Print to terminal (or use logger)
        logger.info(f"Image captured and saved successfully: {captured_image.id}")

        return Response({'message': 'Image uploaded successfully', 'id': captured_image.id}, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
