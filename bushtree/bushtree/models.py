import uuid
from django.db import models 

class Seccion(models.Model):
    """Запись сессии"""
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    date = models.TextField()
class Flowers(models.Model): 
    """Форма цветника для получения базы данных"""
    #Обновить таблицу
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    #Освещенность и влажность, морозостойкость
    frost_resistance_zone = models.IntegerField()
    light = models.TextField()
    watering = models.TextField() #Режим полива
    #Цвета
    color_main = models.TextField()
    color_other = models.TextField()
    #Период цветения
    period_bloosom_start = models.IntegerField()
    period_bloosom_end = models.IntegerField()

class Gardens(models.Model):
    """Форма передачи данных для получения инфорации по цветникам/цветам"""
    id = models.AutoField(primary_key=True)
    gardens = models.CharField(max_length=255)


