# Generated by Django 4.2.6 on 2023-10-18 05:39

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                ("code", models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name="市区町村コード")),
                ("name", models.CharField(max_length=20, verbose_name="市区町村名")),
                ("geom", django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name="ジオメトリ")),
            ],
            options={
                "verbose_name": "市区町村",
                "verbose_name_plural": "市区町村",
                "ordering": ["code"],
            },
        ),
    ]
