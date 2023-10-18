import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, Self, Tuple

import shapefile
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from ...models import City


class Command(BaseCommand):
    """市区町村モデルインスタンスをシェイプファイルで入れ替え。"""

    # --file引数を省略した場合のデフォルトのシェイプファイルのパス
    path = "resources/cities/cities.shp"
    # シェイプファイルのフィールド
    FIELDS = [
        {"name": "city_code", "type": "C"},
        {"name": "pref_code", "type": "C"},
        {"name": "pref_name", "type": "C"},
        {"name": "city_name", "type": "C"},
    ]

    def handle(self: Self, *args: list[str], **options: dict[str, str]) -> None:
        """
        コマンドを実行する。

        Args:
        ----
            *args (list[str]): コマンドライン引数
            **options (dict[str, str]): コマンドラインオプション
        """
        # シェイプファイルの存在を確認
        shp_path = options["file"]
        if not self.exists_file(shp_path):
            raise CommandError(f"シェイプファイルが存在しません。{shp_path}")
        # トランザクションを開始
        try:
            with transaction.atomic():
                # すべての市区町村モデルインスタンスを削除
                self.delete_all_cities()
                # 市区町村モデルインスタンスをシェイプファイルから登録
                self.register_cities_from_shapefile(shp_path, options["encoding"])
                # 成功した場合はトランザクションをコミット
        except:
            # 失敗した場合はトランザクションをロールバック
            raise

    def delete_all_cities(self) -> None:
        """市区町村モデルインスタンスをすべて削除する。"""
        City.objects.all().delete()

    def register_cities_from_shapefile(self, path: str, encoding: str) -> None:
        """
        シェイプファイルを読み込み、市区町村モデルインスタンスを入れ替える。

        Args:
            path (str): シェイプファイルのパス
            encoding (str): シェイプファイルのエンコーディング
        """
        with shapefile.Reader(path, encoding=encoding) as reader:
            # シェイプファイルを検証
            self.validate_shapefile(reader)
            # フィーチャを読み込み、市区町村モデルインスタンスを登録
            for feature in reader.iterShapeRecords():
                city = self.build_city_from_feature(feature)
                city.save()

    def build_city_from_feature(self, feature: shapefile.ShapeRecord) -> City:
        """フィーチャーから市区町村モデルインスタンスを構築する。

        feature.shape.partsには、ポリゴンの始点のインデックスが格納されている。
        たとえば、feature.shape.partsが[0, 3, 6]の場合、feature.shape.points[0:3]が最初のポリゴン、
        feature.shape.points[3:6]が次のポリゴン、feature.shape.points[6:]が最後のポリゴンとなる。

        Args:
            feature (shapefile.ShapeRecord): シェイプファイルフィーチャ

        Returns:
            City: 市区町村モデルインスタンス
        """
        polygons: list[Polygon] = []
        if len(feature.shape.parts) == 1:
            polygons.append(Polygon(feature.shape.points))
        else:
            index = 0
            for part in feature.shape.parts[1:]:
                polygons.append(Polygon(feature.shape.points[index:part]))
                index = part
            polygons.append(Polygon(feature.shape.points[index:]))
        geometry = MultiPolygon(polygons)
        city = City()
        city.code = feature.record["city_code"]
        city.pref_code = feature.record["pref_code"]
        city.pref_name = feature.record["pref_name"]
        city.name = feature.record["city_name"]
        city.geom = geometry
        return city

    def validate_shapefile(self, reader: shapefile.Reader) -> None:
        """シェイプファイルを検証する。

        Args:
            reader (shapefile.Reader): シェイプファイルリーダー

        Returns:
            None

        Raises:
            CommandError
        """
        # シェイプファイルのジオメトリを検証
        if reader.shapeType != shapefile.POLYGON:
            raise CommandError("シェイプファイルのジオメトリがマルチポリゴンではありません。")
        # シェイプファイルのフィールドの名前と型を取得
        for field in self.FIELDS:
            dbf_field = self.find_shapefile_field(reader, field["name"])
            if dbf_field is None:
                raise CommandError(f"シェイプファイルに{field['name']}フィールドがありません。")
            if dbf_field[1] != field["type"]:
                raise CommandError(f"シェイプファイルの{field['name']}フィールドの型が、{field['type']}ではありません。")

    def find_shapefile_field(self, reader: shapefile.Reader, name: str) -> Optional[Tuple]:
        """シェイプファイルの主題属性フィールドを検索する。

        Args:
            reader (shapefile.Reader): シェイプファイルリーダー
            name (str): 検索する主題属性フィールドの名前

        Returns:
            Optional[shapefile.Field]: 主題属性フィールド。見つからなかった場合はNone。
        """
        for field in reader.fields[1:]:
            if field[0] == name:
                return field
        return None

    def add_arguments(self: Self, parser: ArgumentParser) -> None:
        """
        コマンドライン引数を追加する。

        Args:
        ----
            parser (ArgumentParser): コマンドライン引数パーサー
        """
        parser.add_argument("--file", type=str, default=self.path, help="シェイプファイルのパス")
        parser.add_argument("--encoding", type=str, default="utf-8", help="シェイプファイルのエンコーディング")

    def exists_file(self: Self, path: str) -> bool:
        """
        シェイプファイルが存在するか確認する。

        Args:
        ----
            path (str): シェイプファイルのパス

        Returns:
        -------
            bool: シェイプファイルが存在する場合はTrue。存在しない場合はFalse。
        """
        shp_path = Path(path)
        if not shp_path.is_file():
            return False
        base_name, _ = os.path.splitext(path)
        shx_path = Path(f"{base_name}.shx")
        if not shx_path.is_file():
            return False
        dbf_path = Path(f"{base_name}.dbf")
        return dbf_path.is_file()
