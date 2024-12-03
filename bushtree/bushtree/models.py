import uuid
from django.db import models 
class Flower(models.Model): 
    """Цветы, используемые для рассады на цветниках. Полная информация"""
    #Обновить таблицу
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    #Освещенность и влажность, морозостойкость
    frost_resistance_zone = models.IntegerField()
    light = models.TextField(null=True)
    watering = models.TextField(null=True) #Режим полива
    #Цвета
    color_main = models.TextField(null=True)
    color_other = models.TextField(null=True)
    #Период цветения
    period_bloosom_start = models.IntegerField(null=True)
    period_bloosom_end = models.IntegerField(null=True)
    #Дополнительная информация
    decorative_terms_start = models.TextField(null=True)
    decorative_terms_end = models.TextField(null=True)
    flower_color = models.TextField(null=True)
    leaf_color = models.TextField(null=True)
    storage_before_planting = models.TextField(null=True)
    landing_place = models.TextField(null=True)
    soil_requirements = models.TextField(null=True)
    boarding = models.TextField(null=True)
    care = models.TextField(null=True)
    reproduction = models.TextField(null=True)
    use_in_landscape_design = models.TextField(null=True)
    cleaning_for_the_winter = models.TextField(null=True)
    shelter_for_the_winter = models.TextField(null=True)
    winter_hardiness = models.TextField(null=True)
    keeping = models.TextField(null=True)

class FlowerDataset(models.Model):
    "Цветы, необходимые для выбора карты рассадки. Аналоги цветов находятся в Flower"
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=True)
    frost_resistance_zone = models.IntegerField(null=True)
    light = models.TextField(null=True)
    watering = models.TextField(null=True)
    color_main = models.TextField(null=True)
    color_other = models.TextField(null=True)
    decorative_terms_start = models.IntegerField(null=True)
    decorative_terms_end = models.IntegerField(null=True)
    height_from = models.IntegerField(null=True)
    height_to = models.IntegerField(null=True)
    expansion_id = models.IntegerField(null=True)
class Garden(models.Model):
    """Фотографии цветников. Хранение на стороне сервера"""
    id = models.AutoField(primary_key=True)
    garden_id = models.IntegerField(default=0)
    gardens = models.FileField(upload_to="garden/", max_length=100)

class FlowerBand(models.Model):
    """Карта рассадки цветов по номерам. mass - количество цветов, необходимое для карты рассадки"""
    id = models.AutoField(primary_key=True)
    flower_band_id = models.IntegerField(default=0)
    mass = models.PositiveIntegerField()
    flower_band = models.FileField(upload_to="flowerband/", max_length=100)


