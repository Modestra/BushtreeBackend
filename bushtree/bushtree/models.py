import uuid
from django.db import models 

class Flowers(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.TextField(null=False)
    description = models.TextField(null=False)
    frozen_resistance = models.CharField(max_length=5)
    sunlight = models.CharField(max_length=20)
    period_blossom_start = models.TextField(null=False)
    period_blossom_end = models.TextField(null=False)
    height = models.PositiveBigIntegerField(default=0)
    color_bloss_name = models.CharField(max_length=20)
    color_bloss_hex = models.CharField(max_length=8)
    color_leaves_name = models.CharField(max_length=20)
    color_leaves_hex = models.CharField(max_length=8)

