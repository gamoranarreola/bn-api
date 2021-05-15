import json
import random
from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_auth_users(apps, schema_editor):

    auth_user_model = apps.get_model('bn_app', 'AuthUser')
    customer_profile_model = apps.get_model('bn_app', 'CustomerProfile')

    auth_users_json = json.loads(open('bn_utils/data/json/users.json').read())

    for auth_user in auth_users_json:

        auth_user = auth_user_model(
            password=make_password(auth_user['password']),
            is_superuser=auth_user['is_superuser'],
            first_name=auth_user['first_name'],
            last_name=auth_user['last_name'],
            email=auth_user['email'],
            phone=auth_user['phone'],
            is_staff=auth_user['is_staff'],
            is_active=auth_user['is_active']
        )

        auth_user.save()
        print(f'CUSTOM USER: {auth_user}\n')

        customer_profile = customer_profile_model(
            auth_user=auth_user_model.objects.get(pk=auth_user.id),
            customer_profile_id=f'C{auth_user.id * 2 + 100}'
        )

        customer_profile.save()
        print(f'CUSTOMER PROFILE: {customer_profile}\n')

def seed_beautiers(apps, schema_editor):

    auth_user_model = apps.get_model('bn_app', 'AuthUser')
    beautier_profile_model = apps.get_model('bn_app', 'BeautierProfile')
    beautiers_json = json.loads(open('bn_utils/data/json/beautiers.json').read())

    for beautier_profile in beautiers_json:

        beautier_profile = beautier_profile_model(
            auth_user=auth_user_model.objects.get(pk=beautier_profile['auth_user_id']),
            calendar_id=beautier_profile['calendar_id'],
            availability=beautier_profile['availability']
        )

        beautier_profile.save()
        print(f'BEAUTIER PROFILE: {beautier_profile}\n')


def seed_beautier_profile_specialties(apps, schema_editor):

    beautier_profile_model = apps.get_model('bn_app', 'BeautierProfile')
    beautier_profile_specialty_model = apps.get_model('bn_app', 'BeautierProfileSpecialty')

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

    service_category_model = apps.get_model('bn_app', 'ServiceCategory')
    service_categories_json = json.loads(open('bn_utils/data/json/service-categories.json').read())

    for item in service_categories_json:

        service_category = service_category_model(
            id=item['id'],
            name=item['name']
        )

        service_category.save()
        print(f'SERVICE CATEGORY: {service_category}\n')


def seed_specialties(apps, schema_editor):

    specialty_model = apps.get_model('bn_app', 'Specialty')
    specialties_json = json.loads(open('bn_utils/data/json/specialties.json').read())

    for item in specialties_json:

        specialty = specialty_model(
            id=item['id'],
            name=item['name']
        )

        specialty.save()
        print(f'SPECIALTY: {specialty}\n')


def seed_services(apps, schema_editor):

    service_model = apps.get_model('bn_app', 'Service')
    services_json = json.loads(open('bn_utils/data/json/services.json').read())

    service_category_model = apps.get_model('bn_app', 'ServiceCategory')
    service_specialty_model = apps.get_model('bn_app', 'ServiceSpecialty')

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
        ('bn_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_auth_users),
        migrations.RunPython(seed_beautiers),
        migrations.RunPython(seed_beautier_profile_specialties),
        migrations.RunPython(seed_service_categories),
        migrations.RunPython(seed_specialties),
        migrations.RunPython(seed_services)
    ]
