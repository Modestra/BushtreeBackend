from django.contrib import admin
from bushtree.models import *

class SeccionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Seccion, SeccionAdmin)

class FlowersAdmin(admin.ModelAdmin):
    pass

admin.site.register(Flowers, FlowersAdmin)