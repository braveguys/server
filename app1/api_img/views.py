import os
from pathlib import Path

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .classify import classify


class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      t = file_serializer.save()
      # t.file = file path
      # e.g. file_uITwvxC.jfif
      BASE_DIR = Path(__file__).resolve().parent.parent
      MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
      imagepath = os.path.join(MEDIA_ROOT, str(t.file))

      result = classify(imagepath)
      print('Result:\t', result)

      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)