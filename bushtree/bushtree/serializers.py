from rest_framework import serializers
from bushtree.models import *

class FlowerSerializer(serializers.ModelSerializer):
    """Форма для запроса необходимого цветника"""
    class Meta:
        model = Flower
        fields = '__all__'

class GardenSerializer(serializers.ModelSerializer):
    """Форма для получения данных по цветам/цветникам"""
    
    class Meta:
        model = Garden
        fields = "__all__"