from typing import ClassVar, Self

from django.contrib.gis.db import models as geo_models


class City(geo_models.Model):
    """市区町村モデル"""

    code = geo_models.CharField("市区町村コード", max_length=5, primary_key=True)
    name = geo_models.CharField("市区町村名", max_length=20)
    geom = geo_models.MultiPolygonField("ジオメトリ", srid=4326)

    class Meta:
        verbose_name: ClassVar[str] = "市区町村"
        verbose_name_plural: ClassVar[str] = "市区町村"
        ordering: ClassVar[[list[str]]] = ["code"]

    def __str__(self: Self) -> str:
        """
        市区町村名を返却する。

        Args:
        ----
            self (Self): モデルインスタンス

        Returns:
        -------
            str: 市区町村名
        """
        return self.name
