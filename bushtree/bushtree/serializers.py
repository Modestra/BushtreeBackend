from rest_framework import serializers
from bushtree.models import *

class FlowerSerializer(serializers.Serializer):
    """Форма для запроса необходимого цветника"""
    frost_resistance_zone = serializers.CharField(max_length=255)
    light = serializers.CharField(max_length=255)
    watering = serializers.CharField(max_length=255)
    color_main = serializers.CharField(max_length=255)
    color_other = serializers.CharField(max_length=255)
    period_bloosom_start = serializers.CharField(max_length=255)
    period_bloosom_end = serializers.CharField(max_length=255)

    def validate(self, attrs):
        return super().validate(attrs)
    
class FlowerBandDeleteSerializer(serializers.Serializer):
    flower_band_id = serializers.CharField(max_length=255)
    
    def validate(self, attrs):
        return super().validate(attrs)
    
class FlowerBandSerializer(serializers.Serializer):
    flower_band_id = serializers.CharField(max_length=255, read_only=True)
    mass = serializers.CharField(max_length=255)
    flower_band = serializers.FileField()

    regex_mask = '/[0-9]+\.(?:jpg|png)/g'
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        flower_band = validated_data.get("flower_band", None)
        _flower_band_id = str(flower_band).split(".")[0]
        return FlowerBand.objects.create(flower_band_id=_flower_band_id, **validated_data)

class GardenSerializer(serializers.Serializer):
    """Форма для получения данных по цветам/цветникам"""
    garden_id = serializers.CharField(max_length=255)

    def validate(self, attrs):
        return super().validate(attrs)
    