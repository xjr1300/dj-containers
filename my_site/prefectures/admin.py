from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Prefecture


class PrefectureAdmin(OSMGeoAdmin):
    fields = ("code", "name")
    list_display = ("code", "name")
    ordering = ("code",)
    list_display_links = ("code",)
    search_fields = (
        "code",
        "name",
    )


admin.site.register(Prefecture, PrefectureAdmin)
