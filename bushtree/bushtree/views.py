from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import action
from bushtree.serializers import *
from bushtree.models import *
from bushtree.mixin import *
import os
from django.forms.models import model_to_dict
from django.conf import settings
from bushtree.dataset import FlowersSet

def get_info_flowers(flowers : list):
    flower_list = []
    for f in flowers:
        flower = Flower.objects.filter(name=f).first()
        flower = model_to_dict(flower)
        flower_list.append(flower)
    return flower_list

class FlowerApiViewSet(ListViewSet):
    """Получить полную информацию по цветам"""
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer
    
    @action(detail=False, methods=["POST"], serializer_class=GardenIdSerializer)
    def near_flowers(self, request):
        serializer = GardenIdSerializer(data=request.data)
        if serializer.is_valid():
            flowers = FlowersSet.GetFlowers(str(serializer.data['garden_id']).split(" "))
            json_flowers = get_info_flowers(flowers=flowers)
            return Response({"flowers_names": ",".join(flowers), "flowers": json_flowers}, status=status.HTTP_200_OK)
        return Response({"error": "Не удалось загрузить данные. Невалидная форма"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], serializer_class=ColorSerializer)
    def create_garden(self, request):
        serializers = ColorSerializer(data=request.data)
        if serializers.is_valid():
            json_data = FlowersSet.dataset_creategarden(serializers.data["color_main"], serializers.data["color_other"])
            return Response({"gardens": json_data}, status=status.HTTP_200_OK)
    
class GardensApiViewSet(ListViewSet):
    """Фотографии готовых цветников. Основная модель взаимодействия"""
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    parser_classes = [JSONParser, MultiPartParser]
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(parser_classes=MultiPartParser)
    @action(detail=False, methods=["post"], serializer_class=GardenSerializer, parser_classes=[MultiPartParser])
    def load_image(self, request):
        serializers = GardenSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Не удалось создать файл в media"}, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=GardenIdSerializer)
    @action(detail=False, methods=["delete"], serializer_class=GardenIdSerializer)
    def delete_image(self, request):
        serializers = GardenIdSerializer(data=request.data)
        if serializers.is_valid():
            flowerband_url = os.path.join(settings.MEDIA_ROOT, f"garden/{serializers.data["garden_id"]}.png")
            files = Garden.objects.filter(garden_id=serializers.data["garden_id"]).delete()
            if os.path.exists(flowerband_url):
                os.remove(flowerband_url)
                return Response({"success": "Файл удален"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Не удалось найти файл в media"}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({"error": "Некорректный запрос"}, status=status.HTTP_400_BAD_REQUEST)
    

class FlowerBandApiViewSet(ListViewSet):
    queryset = FlowerBand.objects.all()
    serializer_class = FlowerBandSerializer
    parser_classes=(JSONParser, MultiPartParser)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(parser_classes=MultiPartParser)
    @action(detail=False, methods=["post"], serializer_class=FlowerBandSerializer, parser_classes=[MultiPartParser])
    def load_image(self, request):
        serializers = FlowerBandSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Не удалось создать файл в media"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=FlowerBandIdSerializer)
    @action(detail=False, methods=["delete"], serializer_class=FlowerBandIdSerializer)
    def delete_image(self, request):
        serializers = FlowerBandIdSerializer(data=request.data)
        if serializers.is_valid():
            flowerband_url = os.path.join(settings.MEDIA_ROOT, f"flowerband/{serializers.data["flower_band_id"]}.png")
            files = FlowerBand.objects.filter(flower_band_id=serializers.data["flower_band_id"]).delete()
            if os.path.exists(flowerband_url):
                os.remove(flowerband_url)
                return Response({"success": "Файл удален"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Некорректный запрос"}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({"error": "Не удалось найти файл в media"}, status=status.HTTP_400_BAD_REQUEST)
    
    
        