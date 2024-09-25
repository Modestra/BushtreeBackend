from rest_framework import serializers
from bushtree.models import *

class FlowerSerializer(serializers.ModelSerializer):
    """Форма для запроса необходимого цветника"""
    class Meta:
        model = Flowers
        fields = '__all__'

class SeccionSerializer(serializers.ModelSerializer):
    """Форма для получения данных сессии"""
    
    class Meta:
        model = Seccion
        fields = "__all__"
