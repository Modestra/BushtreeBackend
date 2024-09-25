from rest_framework import (status, viewsets)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action
from bushtree.serializers import *
from bushtree.models import *
from bushtree.mixin import *
import nbconvert, nbformat, requests, codecs
from django.conf import settings
from bushtree.dataset import dataset_creategarden

class FlowerApiViewSet(viewsets.ModelViewSet):
    
    queryset = Flowers.objects.all()
    serializer_class = FlowerSerializer

    def list(self, request, *args, **kwargs):
        json_data = dataset_creategarden()
        return Response({"data": json_data}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        json_data = dataset_creategarden()
        return Response({"data": json_data}, status=status.HTTP_200_OK)
    

class SeccionsApiViewSet(viewsets.ModelViewSet):

    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    
        