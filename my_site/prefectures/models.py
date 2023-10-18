from typing import ClassVar, Self

from django.contrib.gis.db import models as geomodels


class Prefecture(geomodels.Model):
    """都道府県モデル"""

    code = geomodels.CharField("都道府県コード", max_length=2, primary_key=True)
    name = geomodels.CharField("都道府県名", max_length=10)
    geom = geomodels.MultiPolygonField("ジオメトリ", srid=4326)

    class Meta:
        db_table: ClassVar[str] = "prefectures"
        verbose_name: ClassVar[str] = "都道府県"
        verbose_name_plural: ClassVar[str] = "都道府県"
        ordering: ClassVar[list[str]] = ["code"]

    def __str__(self: Self) -> str:
        return self.name
