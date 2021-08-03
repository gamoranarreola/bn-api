from bn_app.models import CustomerProfile, AuthUser, Service, WorkOrder, LineItem
import pytest


@pytest.mark.django_db(transaction=True)
def test_create_work_order(api_client_with_credentials, create_service):

    create_service()
    services = Service.objects.all()

    res = api_client_with_credentials.post(
        path='/api/work-orders',
        data={
            'request_date': '2020-09-01',
            'request_time': '06:00 AM',
            'place_id': 'e7e0a378-323f-43c6-8029-39b60599a919',
            'customer_profile_id': CustomerProfile.objects.get(auth_user=AuthUser.objects.get(email='test_user@test.com')).id,
            'notes': 'Some notes',
            'status': 'initial_request',
            'line_items': [
                {
                    'service': services[0].id,
                    'service_date': '2020-09-02',
                    'service_time': '09:00 AM',
                    'quantity': 1,
                    'price': 800
                },
                {
                    'service': services[0].id,
                    'service_date': '2020-09-02',
                    'service_time': '09:30 AM',
                    'quantity': 1,
                    'price': 800
                }
            ]
        },
        format='json'
    )

    assert WorkOrder.objects.filter(pk=res.data.get('data').get('id')).exists() == True
    assert len(LineItem.objects.all()) == 2
    assert res.data.get('status') == 200
