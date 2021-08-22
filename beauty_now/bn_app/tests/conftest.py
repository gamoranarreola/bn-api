from bn_app.serializers import StaffAssigmentSerializer

from bn_app.models import (
    Service,
    ServiceCategory,
    WorkOrder,
    AuthUser,
    CustomerProfile,
    LineItem,
    StaffingAssignment,
    BeautierProfile)

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


@pytest.fixture
def create_work_order(create_service):
    def make_work_order():
        service = create_service()

        work_order = WorkOrder.objects.create(
            request_date='2020-09-01',
            request_time='06:00 AM',
            place_id='e7e0a378-323f-43c6-8029-39b60599a919',
            customer_profile_id=CustomerProfile.objects.get(auth_user=AuthUser.objects.get(email='test_user@test.com')).id,
            notes='Some notes',
            status='initial_request'
        )

        line_items = [
            {
                'service': service.id,
                'service_date': '2020-09-02',
                'service_time': '09:00 AM',
                'quantity': 3,
                'price': 800
            },
            {
                'service': service.id,
                'service_date': '2020-09-02',
                'service_time': '09:30 AM',
                'quantity': 2,
                'price': 800
            }
        ]

        for line_item in line_items:
            work_order.line_items.add(LineItem.objects.create(
                service=Service.objects.get(pk=line_item['service']),
                service_date=line_item['service_date'],
                service_time=line_item['service_time'],
                quantity=line_item['quantity'],
                price=line_item['price']
            ))

        return work_order
    return make_work_order


@pytest.fixture
def create_staffing_assignments(create_work_order):
    def make_staffing_assignment():
        work_order = create_work_order()
        staffing_assignments = []

        for line_item in work_order.line_items.all():

            for i in range(1, line_item.quantity + 1):

                staffing_assignment = StaffAssigmentSerializer(StaffingAssignment.objects.create(
                    line_item=line_item,
                    index=i
                ))

                staffing_assignments.append(staffing_assignment.data)

        return staffing_assignments
    return make_staffing_assignment


@pytest.fixture
def create_beautier():
    def make_beautier():
        beautier = BeautierProfile.objects.create(
            auth_user=AuthUser.objects.get(email='test_user@test.com')
        )

        return beautier
    return make_beautier
