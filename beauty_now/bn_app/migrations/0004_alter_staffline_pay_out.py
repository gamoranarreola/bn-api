# Generated by Django 3.2.5 on 2021-08-31 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bn_app', '0003_auto_20210824_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffline',
            name='pay_out',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
