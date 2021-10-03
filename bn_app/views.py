from requests.api import post
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import googlemaps
import conekta
from uritemplate.api import partial

conekta.api_key = 'key_qrXw7xpD26Czohm81ErhrA'
conekta.locale = 'es'
conekta.api_version = "2.5.1"

from bn_utils.google.google import (
    get_calendar_service,
    handle_calendar_params,
    handle_free_busy_data,
    handle_events_data
)

from .models import (
    AuthUser,
    BeautierProfile,
    Service,
    ServiceCategory,
    CustomerProfile,
    CustomerProfileAddress,
    StaffAssignment,
    StaffLine,
    WorkOrder
)

from .serializers import (
    CustomerProfileSerializer,
    LineItemSerializer,
    MeSerializer,
    BeautierProfileSerializer,
    ServiceSerializer,
    ServiceCategorySerializer,
    StaffAssigmentSerializer,
    StaffLineSerializer,
    WorkOrderSerializer,
    CustomerProfileAddressSerializer
)

from bn_utils.responses.generic_responses import (
    response_200,
    response_201,
    response_204,
    response_400,
    response_500
)

from bn_core.tasks import handle_initial_work_order_request


class UserActivationView(APIView):

    def get(self, request, uid, token):

        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + '/api/auth/users/activation/'
        post_data = {'uid': uid, 'token': token}
        result = post(post_url, data=post_data)

        return Response(result.status_code)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def me(request):

    try:

        auth_user = AuthUser.objects.get(pk=request.user.id)
        serializer = MeSerializer(auth_user, many=False)

        return response_200(serializer.data)

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['GET'])
def beautiers(request):

    try:

        beautiers = BeautierProfile.objects.all()
        serializer = BeautierProfileSerializer(beautiers, many=True)

        return response_200(serializer.data)

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['GET'])
def beautier_by_id(request, pk):

    try:

        beautier = BeautierProfile.objects.get(pk=pk)
        serializer = BeautierProfileSerializer(beautier, many=False)

        return response_200(serializer.data)

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['POST'])
def beautiers_for_specialties(request):

    try:

        beautiers_for_specialties = BeautierProfile.objects.filter(specialties__in=request.data['specialty_ids']).distinct()
        serializer = BeautierProfileSerializer(beautiers_for_specialties, many=True)

        return response_200(serializer.data)

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['GET'])
def service_by_id(request, pk):

    try:

        service = Service.objects.get(pk=pk)
        serializer = ServiceSerializer(service, many=False)

        return response_200(serializer.data)

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['GET'])
def service_by_category_id(request, service_category_id):

    try:

        services = Service.objects.filter(category_id=service_category_id)
        serializer = ServiceSerializer(services, many=True)

        return response_200(serializer.data)

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['GET'])
def service_categories(request):

    try:

        serviceCategories = ServiceCategory.objects.all()
        serializer = ServiceCategorySerializer(serviceCategories, many=True)

        return response_200(serializer.data)

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['GET'])
def service_category_by_id(request, pk):

    try:

        serviceCategory = ServiceCategory.objects.get(pk=pk)
        serializer = ServiceCategorySerializer(serviceCategory, many=False)

        return response_200(serializer.data)

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['POST'])
def calendars_for_beautiers(request):

    try:

        service = get_calendar_service()
        calendar_data = []

        for id in request.data['calendarIds']:

            free_busy_request_body = {
                'timeMin': request.data['timeMin'],
                'timeMax': request.data['timeMax'],
                'items': [
                    {'id': id}
                ],
                'timeZone': 'America/Los_Angeles'
            }

            calendar_data.append({
                'calendar': handle_calendar_params(service.calendars().get(calendarId=id).execute()),
                'free_busy': handle_free_busy_data(service.freebusy().query(body=free_busy_request_body).execute(), id),
                'events': handle_events_data(service.events().list(calendarId=id).execute()),
            })

        return response_200(calendar_data)

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def handle_payment(request):

    try:

        auth_user = AuthUser.objects.get(pk=request.user.id)

        customer = conekta.Customer.create({
            'name': request.data.get('customer')['name'],
            'metadata': {
                'description': 'Compra de Servicios'
            },
            'payment_sources': request.data.get('customer')['payment_sources']
        })

        line_items = []

        for line_item in request.data.get('work_order')['line_items']:

            line_items.append({
                'name': line_item['service']['name'],
                'unit_price': line_item['price'],
                'quantity': line_item['quantity'],
            })

        order = conekta.Order.create({
            'line_items': line_items,
            'currency': 'mxn',
            'customer_info': {
                'customer_id': customer.id,
            },
            'metadata': {
                'description': 'Compra de Servicio(s)'
            },
            'charges': [{
                'payment_method': {
                    'type': 'default'
                }
            }]
        })

        if order.payment_status == 'paid':

            work_order_serializer = WorkOrderSerializer(data={
                'request_date': request.data.get('work_order')['request_date'],
                'request_time': request.data.get('work_order')['request_time'],
                'place_id': request.data.get('work_order')['place_id'],
                'customer_profile': CustomerProfile.objects.get(auth_user=auth_user).id,
                'notes': request.data.get('work_order')['notes'],
                'status': request.data.get('work_order')['status'],
            })

            if work_order_serializer.is_valid():

                work_order_instance = work_order_serializer.save()

                for line_item in request.data.get('work_order')['line_items']:

                    line_item_serializer = LineItemSerializer(data={
                        'service': Service.objects.get(pk=line_item.get('service')['id']).id,
                        'service_date': line_item['service_date'],
                        'service_time': line_item['service_time'],
                        'quantity': line_item['quantity'],
                        'price': line_item['price'],
                    })

                    if line_item_serializer.is_valid():

                        line_item_instance = line_item_serializer.save()
                        work_order_instance.line_items.add(line_item_instance)

                if not CustomerProfileAddress.objects.filter(customer_profile=CustomerProfile.objects.get(auth_user=auth_user.id)).filter(place_id=request.data.get('work_order')['place_id']).exists():

                    customer_profile_address_serializer = CustomerProfileAddressSerializer(data={
                        'customer_profile': CustomerProfile.objects.get(auth_user=auth_user).id,
                        'place_id': request.data.get('work_order')['place_id']
                    })

                    if customer_profile_address_serializer.is_valid():
                        customer_profile_address_serializer.save()

            return response_200({
                'payment_status': order.payment_status,
                'payment_amount': f'${str((order.amount / 100))} {order.currency}',
                'payment_method': {
                    'brand': order.charges[0].payment_method.brand,
                    'last4': order.charges[0].payment_method.last4,
                }
            })

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def work_orders(request):

    try:

        if request.method == 'GET':

            work_orders = WorkOrder.objects.filter(customer_profile=CustomerProfile.objects.get(auth_user=request.user.id))
            serializer = WorkOrderSerializer(work_orders, many=True)

            return response_200(serializer.data)

        elif request.method == 'POST':

            with transaction.atomic():

                work_order_savepoint = transaction.savepoint()

                work_order_serializer = WorkOrderSerializer(data={
                    'request_date': request.data.get('request_date'),
                    'request_time': request.data.get('request_time'),
                    'customer_profile_id': CustomerProfile.objects.get(auth_user_id=AuthUser.objects.get(pk=request.user.id)).id,
                    'place_id': request.data.get('place_id'),
                    'notes': request.data.get('notes'),
                    'status': request.data.get('status'),
                    'line_items': request.data.get('line_items')
                })

                if work_order_serializer.is_valid():

                    work_order_instance = work_order_serializer.save()
                    transaction.savepoint_commit(work_order_savepoint)
                    line_items_savepoint = transaction.savepoint()

                    for line_item in request.data.get('line_items'):

                        line_item_instance = work_order_instance.line_items.create(
                            service=Service.objects.get(pk=line_item['service_id']),
                            service_date=line_item['service_date'],
                            service_time=line_item['service_time'],
                            quantity=line_item['quantity'],
                            price=line_item['price']
                        )

                        for idx in range(1, line_item['quantity'] + 1):

                            staff_assignment_instance = line_item_instance.staff_assignments.create(
                                line_item=line_item_instance,
                                index=idx
                            )

                            staff_assignment_instance.staff_lines.create(staff_assignment=staff_assignment_instance)

                    transaction.savepoint_commit(line_items_savepoint)
                    return response_201(work_order_serializer.data)

                return response_400()

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def get_formatted_address(request):

    google_maps_client = googlemaps.Client(key='AIzaSyAP1kEvf4GgsAVLzI2MLGKpi1w17nmNDTQ')

    try:

        response = google_maps_client.place(request.data['place_id'])
        return response_200(response['result']['formatted_address'])

    except Exception as err:
        return response_500(err)


"""
ADMIN ENDPOINTS
"""

@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_customer_profiles(request):

    try:

        customer_profile_serializer = CustomerProfileSerializer(CustomerProfile.objects.all(), many=True)

        return response_200(customer_profile_serializer.data);

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_work_orders(request):

    try:

        work_orders = WorkOrder.objects.all()
        work_orders_serializer = WorkOrderSerializer(work_orders, many=True)

        return response_200(work_orders_serializer.data)

    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_staff_assignments(request):

    try:

        staff_assignments = StaffAssignment.objects.filter(line_item_id=request.data.get('line_item_id'))
        serializer = StaffAssigmentSerializer(staff_assignments, many=True)

        return response_200(serializer.data)


    except Exception as err:
        return response_500(err)


@api_view(http_method_names=['POST', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_staff_lines(request, pk=None):

    try:

        if request.method == 'POST':

            staff_assignment = StaffAssignment.objects.get(pk=request.data.get('staff_assignment_id'))
            staff_line_serializer = StaffLineSerializer(staff_assignment.staff_lines.create(staff_assignment=staff_assignment))

            return response_201(staff_line_serializer.data)

        elif request.method == 'DELETE':

            staff_line = StaffLine.objects.get(pk=pk)
            staff_line.delete();

            return response_204({})

        elif request.method == 'PATCH':

            data = {}

            if 'auth_user_id' in request.data:
                data['auth_user'] = AuthUser.objects.get(pk=request.data.get('auth_user_id')).id

            if 'pay_out' in request.data:
                data['pay_out'] = request.data.get('pay_out')

            staff_line_serializer = StaffLineSerializer(instance=StaffLine.objects.get(pk=pk), data=data, partial=True)

            if staff_line_serializer.is_valid():
                staff_line_serializer.save()

                return response_204(staff_line_serializer.data)

    except Exception as err:
        return response_500(err)
