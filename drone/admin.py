from django.contrib import admin

from drone.models import Drone, Part, DroneItem, PartItem

# Register your models here.
admin.site.register(Drone)
admin.site.register(DroneItem)

admin.site.register(Part)

admin.site.register(PartItem)