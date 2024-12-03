from rest_framework import (status, viewsets)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import action
from bushtree.serializers import *
from bushtree.models import *
from bushtree.mixin import *
import os
from django.conf import settings
from bushtree.dataset import FlowersSet

def get_info_flowers(flowers : list):
    flower_list = []
    print(flowers)
    try:
        for flower in flowers:
            temp_flower = flower.strip(" ")
            data_flower = Flower.objects.get(name=temp_flower)
            flower_list.append(FlowerSerializer(data_flower, many=False).data)
    except Flower.DoesNotExist:
        flower_list.append("")
    return flower_list
         

class FlowerApiViewSet(ListViewSet):
    """Получить полную информацию по цветам"""
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer
    
    @action(detail=False, methods=["POST"], serializer_class=GardenSerializer)
    def near_flowers(self, request):
        serializer = GardenSerializer(data=request.data)
        if serializer.is_valid():
            flowers = FlowersSet.GetFlowers(str(serializer.data['garden_id']).split(" ")[0])
            json_flowers = get_info_flowers(flowers=flowers)
            return Response({"flowers_names": ",".join(flowers), "flowers": json_flowers}, status=status.HTTP_200_OK)
        return Response({"error": "Не удалось загрузить данные. Невалидная форма"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], serializer_class=FlowerSerializer)
    def create_garden(self, request):
        serializers = FlowerSerializer(data=request.data)
        if serializers.is_valid():
            json_data = FlowersSet.dataset_creategarden(serializers.data["color_main"], serializers.data["color_other"])
            return Response({"gardens": json_data}, status=status.HTTP_200_OK)
    
class GardensApiViewSet(CreateListViewSet):
    """Фотографии готовых цветников. Основная модель взаимодействия"""
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=False)
        if serializer.is_valid():
            json_data = FlowersSet.dataset_creategarden(serializer.data[""])
            return Response({"gardens": json_data[0]}, status=status.HTTP_200_OK)
        return Response({"error": "Не удалось загрузить данные. Невалидная форма"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], serializer_class=GardenSerializer)
    def create_garden(self, request):
        serializers = GardenSerializer(data=request.data)
        if serializers.is_valid():
            json_data = FlowersSet.dataset_creategarden(serializers.data["color_main"], serializers.data["color_other"])
            return Response({"gardens": json_data}, status=status.HTTP_200_OK)
        return Response({"error": "Некорректный запрос"}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(request_body=GardenSerializer)
    @action(detail=False, methods=["delete"], serializer_class=GardenSerializer)
    def delete_image(self, request):
        serializers = FlowerBandDeleteSerializer(data=request.data)
        if serializers.is_valid():
            flowerband_url = os.path.join(settings.MEDIA_ROOT, f"garden/{serializers.data["garden_id"]}.png")
            files = FlowerBand.objects.filter(flower_band_id=serializers.data["flower_band_id"]).delete()
            if os.path.exists(flowerband_url):
                os.remove(flowerband_url)
                return Response({"success": "Файл удален"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Некорректный запрос"}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({"error": "Не удалось найти файл в media"}, status=status.HTTP_400_BAD_REQUEST)
    

class FlowerBandApiViewSet(CreateListViewSet):
    queryset = FlowerBand.objects.all()
    serializer_class = FlowerBandSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(request_body=FlowerBandDeleteSerializer)
    @action(detail=False, methods=["delete"], serializer_class=FlowerBandDeleteSerializer)
    def delete_image(self, request):
        serializers = FlowerBandDeleteSerializer(data=request.data)
        if serializers.is_valid():
            flowerband_url = os.path.join(settings.MEDIA_ROOT, f"flowerband/{serializers.data["flower_band_id"]}.png")
            files = FlowerBand.objects.filter(flower_band_id=serializers.data["flower_band_id"]).delete()
            if os.path.exists(flowerband_url):
                os.remove(flowerband_url)
                return Response({"success": "Файл удален"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Некорректный запрос"}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({"error": "Не удалось найти файл в media"}, status=status.HTTP_400_BAD_REQUEST)

    
        