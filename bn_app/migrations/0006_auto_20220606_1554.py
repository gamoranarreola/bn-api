# Generated by Django 3.1.14 on 2022-06-06 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bn_app', '0005_auto_20220605_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='category',
        ),
        migrations.AddField(
            model_name='service',
            name='categories',
            field=models.ManyToManyField(to='bn_app.ServiceCategory'),
        ),
    ]