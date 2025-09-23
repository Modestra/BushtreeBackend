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
    height_from = models.IntegerField(null=True)
    height_to = models.IntegerField(null=True)
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
    pruning = models.TextField(null=True)
    winter_hardiness = models.TextField(null=True)
    keeping = models.TextField(null=True)

class FlowerDataset(models.Model):
    #Обновить таблицу
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=True)
    description = models.TextField(null=True)
    #Освещенность и влажность, морозостойкость
    frost_resistance_zone = models.IntegerField(null=True, default=0)
    light = models.TextField(null=True)
    watering = models.TextField(null=True) #Режим полива
    #Цвета
    color_main = models.TextField(null=True)
    color_other = models.TextField(null=True)
    height_from = models.IntegerField(null=True)
    height_to = models.IntegerField(null=True)
    #Дополнительная информация
    decorative_terms_start = models.TextField(null=True)
    decorative_terms_end = models.TextField(null=True)
    cloud_number = models.TextField(null=True)
    flower_beds = models.TextField(null=True)

class Garden(models.Model):
    """Фотографии цветников"""
    id = models.AutoField(primary_key=True)
    flower_id = models.IntegerField(default=0)
    flower_count = models.IntegerField(default=0)
    file = models.FileField(upload_to="gardens/", max_length=100)

class FlowerBand(models.Model):
    """Карта рассадки цветов по номерам"""
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="flowerbands/", max_length=100)

class ImagesModel(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="images/", max_length=100)

class MediaRegistration(models.Model):
    """Регистрация загруженных фотграфий"""
    id = models.AutoField(primary_key=True)
    basedir = models.TextField(null=False)
    filename = models.CharField(max_length=255, null=False)


