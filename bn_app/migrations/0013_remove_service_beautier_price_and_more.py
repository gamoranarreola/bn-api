# Generated by Django 4.0.6 on 2022-07-19 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bn_app", "0012_auto_20220717_1425"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="service",
            name="beautier_price",
        ),
        migrations.RemoveField(
            model_name="service",
            name="beauty_now_price",
        ),
        migrations.RemoveField(
            model_name="service",
            name="public_price",
        ),
    ]
