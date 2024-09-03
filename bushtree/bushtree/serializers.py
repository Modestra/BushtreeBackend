from rest_framework import serializers
from bushtree.models import *

class FlowerSerializer(serializers.ModelSerializer):
    """Форма для запроса необходимого цветника"""
    class Meta:
        model = Flowers
        field = ["name", "description", "frozen_resistance", "sunlight", "period_blossom_start", 
                 "period_blossom_end", "height", "color_bloss_name", "color_bloss_hex", "color_leaves_name", "color_leaves_hex"]

class SeccionSerializer(serializers.ModelSerializer):
    """Форма для получения данных сессии"""
    
    class Meta:
        model = Seccion
        fields = "__all__"
