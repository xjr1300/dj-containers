from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import City


class CityAdmin(OSMGeoAdmin):
    fields = ("code", "name", "geom")
    list_display = ("code", "name")
    ordering = ("code",)
    search_fields = (
        "code",
        "name",
    )


admin.site.register(City, CityAdmin)
