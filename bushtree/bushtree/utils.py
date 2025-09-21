
from enum import Enum
from django.forms import model_to_dict
from bushtree.models import Flower

class MediaDir(Enum):
    FLOWERBAND = "flowerbands"
    GARDENS = "gardens"
    IMAGES = "images"

def get_info_flowers(flowers : list):
    flower_list = []
    for f in flowers:
        flower = Flower.objects.filter(name=f).first()
        flower = model_to_dict(flower)
        flower_list.append(flower)
    return flower_list