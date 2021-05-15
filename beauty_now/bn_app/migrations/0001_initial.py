# Generated by Django 3.2.2 on 2021-05-15 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=128, unique=True)),
                ('phone', models.CharField(blank=True, max_length=64)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BeautierProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar_id', models.CharField(max_length=128, null=True)),
                ('availability', models.JSONField(default=dict)),
                ('auth_user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_profile_id', models.CharField(max_length=10, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auth_user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_date', models.CharField(max_length=10, null=True)),
                ('service_time', models.CharField(max_length=8, null=True)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('beautier_profile', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bn_app.beautierprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('extras', models.CharField(max_length=512)),
                ('includes_eyelashes', models.BooleanField(default=False)),
                ('availability', models.JSONField()),
                ('duration', models.TimeField()),
                ('beautier_price', models.IntegerField()),
                ('beauty_now_price', models.IntegerField()),
                ('public_price', models.IntegerField()),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Service Categories',
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Specialties',
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.CharField(max_length=10, null=True)),
                ('request_time', models.CharField(max_length=8, null=True)),
                ('place_id', models.CharField(max_length=128, null=True)),
                ('notes', models.CharField(blank=True, max_length=256)),
                ('status', models.CharField(default='initial_request', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bn_app.customerprofile')),
                ('line_items', models.ManyToManyField(to='bn_app.LineItem')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceSpecialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bn_app.service')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bn_app.specialty')),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bn_app.servicecategory'),
        ),
        migrations.AddField(
            model_name='service',
            name='specialties',
            field=models.ManyToManyField(through='bn_app.ServiceSpecialty', to='bn_app.Specialty'),
        ),
        migrations.AddField(
            model_name='lineitem',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bn_app.service'),
        ),
        migrations.CreateModel(
            name='CustomerProfileAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_id', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bn_app.customerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='BeautierProfileSpecialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('beautier_profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bn_app.beautierprofile')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bn_app.specialty')),
            ],
            options={
                'verbose_name_plural': 'Beautier Specialties',
            },
        ),
        migrations.AddField(
            model_name='beautierprofile',
            name='specialties',
            field=models.ManyToManyField(through='bn_app.BeautierProfileSpecialty', to='bn_app.Specialty'),
        ),
    ]
