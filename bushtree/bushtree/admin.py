from django.contrib import admin
from bushtree.models import *

class FlowerAdmin(admin.ModelAdmin):
    pass

class FlowerDatasetAdmin(admin.ModelAdmin):
    pass

class FlowerBandAdmin(admin.ModelAdmin):
    pass

class GardenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Flower, FlowerAdmin)
admin.site.register(FlowerDataset, FlowerDatasetAdmin)
admin.site.register(Garden, GardenAdmin)
admin.site.register(FlowerBand, FlowerBandAdmin)