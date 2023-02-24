from django.contrib import admin
from .models import Location,Sensors
# from django.contrib import SensorsAdmin

class SensorsInline(admin.TabularInline):
    model=Sensors
    # exclude=['note']
    extra=0

class LocationAdmin(admin.ModelAdmin):
    fields = ['name', 'memo',]
    inlines=[SensorsInline]
    list_display = ('name', 'memo',)
    list_filter=['name']
    # search_fields=['name']

admin.site.register(Location, LocationAdmin)
# admin.site.register(Location)

admin.site.register(Sensors)
