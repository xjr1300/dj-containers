from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import City


class CityAdmin(OSMGeoAdmin):
    fields = (
        "code",
        "pref_code",
        "pref_name",
        "name",
        "geom",
    )
    list_display = (
        "code",
        "pref_code",
        "pref_name",
        "name",
    )
    ordering = (
        "pref_code",
        "code",
    )
    search_fields = (
        "code",
        "pref_name",
        "name",
    )


admin.site.register(City, CityAdmin)
