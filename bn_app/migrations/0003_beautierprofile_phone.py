# Generated by Django 3.1.14 on 2022-06-05 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bn_app', '0002_auto_20220605_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='beautierprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]