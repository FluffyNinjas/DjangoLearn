from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import UploadedImage
from .serializers import UploadedImageSerializer
from rest_framework.response import Response
from rest_framework import status
from .ai_service import get_image_description


# Create your views here.

class UploadImageView(CreateAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_image = serializer.validated_data['file']
        description = get_image_description(uploaded_image)
        self.perform_create(serializer)
        header = self.get_success_headers(serializer.data)
        return Response({'image_description': description}, status=status.HTTP_201_CREATED, headers=header)