# Generated by Django 3.1.14 on 2022-06-07 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bn_app", "0006_auto_20220606_1554"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="categories",
            field=models.ManyToManyField(
                related_name="service_categories", to="bn_app.ServiceCategory"
            ),
        ),
    ]
