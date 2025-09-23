from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import FileResponse
from bushtree.utils import get_info_flowers
from bushtree.serializers import *
from bushtree.models import *
from bushtree.mixin import *
from django.forms.models import model_to_dict
from django.conf import settings
from bushtree.dataset import FlowersSet
import os

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
    
    @action(detail=False, methods=["post"], serializer_class=ColorSerializer)
    def filter_list(self, request):
        """Отфильтрованные цветы для цветника"""
        serializers = ColorSerializer(data=request.data)
        if serializers.is_valid():
            flowers = Flower.objects.filter(color_main=serializers.data["color_main"], color_other=serializers.data["color_other"])
            return Response({"flowers": [model_to_dict(f, fields=['id', 'name','color_main', 'color_other']) for f in flowers]})
        return Response({"error": "Ошибка"}, status=status.HTTP_400_BAD_REQUEST)
    
class GardensApiViewSet(ListViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    
class MediaApiViewSet(ListViewSet):
    """Взаимодействие с медиа файлами проекта"""
    queryset = MediaRegistration.objects.all()
    serializer_class = MediaImagesSerializer
    parser_classes=(JSONParser, MultiPartParser)


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(parser_classes=MultiPartParser)
    @action(detail=False, methods=["post"], serializer_class=MediaImagesSerializer, parser_classes=[MultiPartParser])
    def load_file(self, request, *args, **kwargs):
        """Загрузка файла в медиа"""
        serializers = MediaImagesSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Не удалось создать файл в media"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["get"], url_path="<base_dir>/<image>")
    def download_file(self, request, *args, **kwargs):
        """Прямая ссылка на файл в медиа запросе"""
        base_dir = kwargs.get("base_dir", None)
        image = kwargs.get("image", None)
        image_url = os.path.join(settings.MEDIA_ROOT, base_dir, image)
        if not os.path.exists(image_url):
            return Response("Image not found", status=404)
        return FileResponse(open(image_url, 'rb'), content_type = 'image/png')
    
        