# Generated by Django 3.1.14 on 2022-06-07 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bn_app', '0008_auto_20220606_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='categories',
        ),
    ]