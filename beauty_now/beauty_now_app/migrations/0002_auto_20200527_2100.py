import json
import random
from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_custom_users(apps, schema_editor):

    custom_user_model = apps.get_model('beauty_now_app', 'CustomUser')
    customer_profile_model = apps.get_model('beauty_now_app', 'CustomerProfile')

    custom_users_json = json.loads(open('beauty_now_utils/database/json/users.json').read())

    for custom_user in custom_users_json:

        custom_user = custom_user_model(
            password=make_password(custom_user['password']),
            is_superuser=custom_user['is_superuser'],
            first_name=custom_user['first_name'],
            last_name=custom_user['last_name'],
            email=custom_user['email'],
            phone=custom_user['phone'],
            is_staff=custom_user['is_staff'],
            is_active=custom_user['is_active']
        )

        custom_user.save()
        print(f'CUSTOM USER: {custom_user}\n')

        customer_profile = customer_profile_model(
            custom_user=custom_user_model.objects.get(pk=custom_user.id),
            customer_profile_id=f'C{custom_user.id * 2 + 100}'
        )

        customer_profile.save()
        print(f'CUSTOMER PROFILE: {customer_profile}\n')

def seed_beautiers(apps, schema_editor):

    custom_user_model = apps.get_model('beauty_now_app', 'CustomUser')
    beautier_profile_model = apps.get_model('beauty_now_app', 'BeautierProfile')
    beautiers_json = json.loads(open('beauty_now_utils/database/json/beautiers.json').read())

    for beautier_profile in beautiers_json:

        beautier_profile = beautier_profile_model(
            custom_user=custom_user_model.objects.get(pk=beautier_profile['custom_user_id']),
            calendar_id=beautier_profile['calendar_id'],
            availability=beautier_profile['availability']
        )

        beautier_profile.save()
        print(f'BEAUTIER PROFILE: {beautier_profile}\n')


def seed_beautier_profile_specialties(apps, schema_editor):

    beautier_profile_model = apps.get_model('beauty_now_app', 'BeautierProfile')
    beautier_profile_specialty_model = apps.get_model('beauty_now_app', 'BeautierProfileSpecialty')

    # Iterate through beautier accounts
    for beautier_profile in beautier_profile_model.objects.all():

        # Generate a random integer from 1 to 4
        number_of_specialties = random.randrange(1, 5, 1)

        # Iterate as many times as the random integer
        for i in range(number_of_specialties):

            # Generate a random integer from 1 to 13 for specialty ID.
            specialty_id = random.randrange(1, 14, 1)

            # Query the beautier_profile_specialty table for an entry that contains the beautier_account_id and the specialty_id.
            query_set = beautier_profile_specialty_model.objects.filter(beautier_profile_id=beautier_profile.id).filter(specialty_id=specialty_id)

            # If the query returns and empty query set, insert the entr.
            if not query_set.exists():

                beautier_profile_specialty = beautier_profile_specialty_model(
                    beautier_profile_id=beautier_profile.id,
                    specialty_id=specialty_id
                )

                beautier_profile_specialty.save()
                print(f'BEAUTIER PROFILE SPECIALTY: {beautier_profile_specialty}\n')


def seed_service_categories(apps, schema_editor):

    service_category_model = apps.get_model('beauty_now_app', 'ServiceCategory')
    service_categories_json = json.loads(open('beauty_now_utils/database/json/service-categories.json').read())

    for item in service_categories_json:

        service_category = service_category_model(
            id=item['id'],
            name=item['name']
        )

        service_category.save()
        print(f'SERVICE CATEGORY: {service_category}\n')


def seed_specialties(apps, schema_editor):

    specialty_model = apps.get_model('beauty_now_app', 'Specialty')
    specialties_json = json.loads(open('beauty_now_utils/database/json/specialties.json').read())

    for item in specialties_json:

        specialty = specialty_model(
            id=item['id'],
            name=item['name']
        )

        specialty.save()
        print(f'SPECIALTY: {specialty}\n')


def seed_services(apps, schema_editor):

    service_model = apps.get_model('beauty_now_app', 'Service')
    services_json = json.loads(open('beauty_now_utils/database/json/services.json').read())

    specialty_model = apps.get_model('beauty_now_app', 'Specialty')
    service_category_model = apps.get_model('beauty_now_app', 'ServiceCategory')
    service_specialty_model = apps.get_model('beauty_now_app', 'ServiceSpecialty')

    for item in services_json:

        service = service_model(
            service_id=item['service_id'],
            category=service_category_model.objects.get(pk=item['category_id']),
            name=item['name'],
            includes_eyelashes=item['includes_eyelashes'],
            availability=item['availability'],
            duration=item['duration'],
            beautier_price=item['beautier_price'],
            beauty_now_price=item['beauty_now_price'],
            public_price=item['public_price']
        )

        service.save()
        print(f'SERVICE: {service}\n')

        for specialty_id in item['specialty_ids']:

            service_specialty = service_specialty_model(
                service_id=service.id,
                specialty_id=specialty_id
            )

            service_specialty.save()
            print(f'SERVICE SPECIALTY: {service_specialty}\n')


class Migration(migrations.Migration):

    """
    Custom migrations
    """
    dependencies = [
        ('beauty_now_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_custom_users),
        migrations.RunPython(seed_beautiers),
        migrations.RunPython(seed_beautier_profile_specialties),
        migrations.RunPython(seed_service_categories),
        migrations.RunPython(seed_specialties),
        migrations.RunPython(seed_services)
    ]
