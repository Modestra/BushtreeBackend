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
from bushtree.dataset import FlowersSet

def get_info_flowers(flowers : list):
    flower_list = []
    print(flowers)
    try:
        for flower in flowers:
            temp_flower = flower.strip(" ")
            data_flower = Flowers.objects.get(name=temp_flower)
            flower_list.append(FlowerSerializer(data_flower, many=False).data)
    except Flowers.DoesNotExist:
        flower_list.append("")
    return flower_list
         

class FlowerApiViewSet(viewsets.ModelViewSet):
    
    queryset = Gardens.objects.all()
    serializer_class = GardenSerializer
    
    @action(detail=True, methods=["POST"])
    def near_flowers(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            flowers = FlowersSet.GetFlowers(str(serializer.data['gardens']).split(" "))
            json_flowers = get_info_flowers(flowers=flowers)
            return Response({"flowers_names": ",".join(flowers), "flowers": json_flowers}, status=status.HTTP_200_OK)
        return Response({"error": "Не удалось загрузить данные. Невалидная форма"}, status=status.HTTP_400_BAD_REQUEST)
    
class GardensApiViewSet(viewsets.ModelViewSet):
    queryset = Flowers.objects.all()
    serializer_class = FlowerSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=False)
        if serializer.is_valid():
            json_data = FlowersSet.dataset_creategarden(serializer.data[""])
            return Response({"gardens": json_data[0]}, status=status.HTTP_200_OK)
        return Response({"error": "Не удалось загрузить данные. Невалидная форма"}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid()
        json_data = FlowersSet.dataset_creategarden(serializers.data["color_main"], serializers.data["color_other"])
        return Response({"gardens": json_data}, status=status.HTTP_200_OK)

class SeccionsApiViewSet(viewsets.ModelViewSet):

    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    
        