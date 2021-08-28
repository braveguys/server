import os
from pathlib import Path

from django.http.response import Http404
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .classify import classify

from .models import State

THRESHOLD = 100

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

      state = State()
      if result < THRESHOLD:
        state.motor = True  
        print('motor true')
      else:
        state.motor = False
        print('motor false')

      state.save()             
      print('Result:\t', result)

      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def open(request):
    state = State()
    state.motor = True
    state.save()
    return HttpResponse("submitted")


def close(request):
    state = State()
    state.motor = False
    state.save()
    return HttpResponse("submitted")


def state(request):
    try:
        state_recent = State.objects.last()
    except:
        raise Http404("no item")

    print('state: ' + str(state_recent))

    if str(state_recent) == 'True':
        return HttpResponse("True")          
    else:
#        return HttpResponse("False")          
        raise Http404("no item")
