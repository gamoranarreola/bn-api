import pytest

from bn_app.models import (
    AuthUser,
    CustomerProfile,
    LineItem,
    Service,
    StaffingAssignment,
    WorkOrder,
)


@pytest.mark.django_db(transaction=True)
def test_create_work_order(api_client_with_credentials, create_service):

    create_service()
    services = Service.objects.all()

    res = api_client_with_credentials.post(
        path="/api/work-orders",
        data={
            "request_date": "2020-09-01",
            "request_time": "06:00 AM",
            "place_id": "e7e0a378-323f-43c6-8029-39b60599a919",
            "customer_profile_id": CustomerProfile.objects.get(
                auth_user=AuthUser.objects.get(email="test_user@test.com")
            ).id,
            "notes": "Some notes",
            "status": "initial_request",
            "line_items": [
                {
                    "service": services[0].id,
                    "service_date": "2020-09-02",
                    "service_time": "09:00 AM",
                    "quantity": 1,
                    "price": 800,
                },
                {
                    "service": services[0].id,
                    "service_date": "2020-09-02",
                    "service_time": "09:30 AM",
                    "quantity": 1,
                    "price": 800,
                },
            ],
        },
        format="json",
    )

    assert WorkOrder.objects.filter(pk=res.data.get("data").get("id")).exists() == True
    assert len(LineItem.objects.all()) == 2
    assert res.data.get("status") == 200


@pytest.mark.django_db()
def test_create_staffing_assignment(api_client_with_credentials, create_work_order):
    work_order = create_work_order()

    res = api_client_with_credentials.post(
        path="/api/staffing-assignment",
        data={"work_order_id": work_order.id},
        format="json",
    )

    assert res.data.get("status") == 200


@pytest.mark.django_db()
def test_create_staffing_assignment_beautier(
    api_client_with_credentials, create_staffing_assignments, create_beautier
):
    staffing_assignments = create_staffing_assignments()
    beautier = create_beautier()

    res = api_client_with_credentials.post(
        path="/api/staffing-assignment/beautier",
        data={
            "staffing_assignment_ids": map(lambda x: x["id"], staffing_assignments),
            "beautier_id": beautier.id,
        },
        format="json",
    )

    for staffing_assignment in staffing_assignments:

        beautier_profiles = StaffingAssignment.objects.get(
            pk=staffing_assignment.get("id")
        ).beautier_profiles.all()
        assert beautier_profiles is not None

    assert res.data.get("status") == 200
