from bn_app.models import Service, ServiceCategory
import pytest

@pytest.fixture
def test_password():
    return '5tr0ngp@55w0rd'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'email' not in kwargs:
            kwargs['email'] = 'test_user@test.com'
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.email, password=test_password)
        return client, user
    return make_auto_login


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    user = create_user()
    api_client.force_authenticate(user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def create_service():
    def make_service():
        service_category = ServiceCategory.objects.create(name="Maquillaje")

        service = Service.objects.create(
            service_id='MQ-SOC-DN',
            category=service_category,
            name='Maquillaje Social Dia o Noche',
            includes_eyelashes=True,
            availability={},
            duration='01:00',
            beautier_price=510,
            beauty_now_price=795,
            public_price=860
        )

        return service
    return make_service
