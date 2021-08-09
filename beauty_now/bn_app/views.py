from requests.api import post
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import googlemaps
import conekta

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
    LineItem,
    Service,
    ServiceCategory,
    CustomerProfile,
    CustomerProfileAddress,
    WorkOrder,
    StaffingAssignment
)

from .serializers import (
    CustomerProfileSerializer,
    LineItemSerializer,
    MeSerializer,
    BeautierProfileSerializer,
    ServiceSerializer,
    ServiceCategorySerializer,
    StaffingAssigmentSerializer,
    WorkOrderSerializer,
    CustomerProfileAddressSerializer
)

from bn_utils.responses.generic_responses import (
    generic_data_response,
    generic_bad_request,
    generic_internal_server_error_response
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

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['GET'])
def beautiers(request):

    try:

        beautiers = BeautierProfile.objects.all()
        serializer = BeautierProfileSerializer(beautiers, many=True)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['GET'])
def beautier_by_id(request, pk):

    try:

        beautier = BeautierProfile.objects.get(pk=pk)
        serializer = BeautierProfileSerializer(beautier, many=False)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['POST'])
def beautiers_for_specialties(request):

    try:

        beautiers_for_specialties = BeautierProfile.objects.filter(specialties__in=request.data['specialty_ids']).distinct()
        serializer = BeautierProfileSerializer(beautiers_for_specialties, many=True)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['GET'])
def service_by_id(request, pk):

    try:

        service = Service.objects.get(pk=pk)
        serializer = ServiceSerializer(service, many=False)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['GET'])
def service_by_category_id(request, service_category_id):

    try:

        services = Service.objects.filter(category_id=service_category_id)
        serializer = ServiceSerializer(services, many=True)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['GET'])
def service_categories(request):

    try:

        serviceCategories = ServiceCategory.objects.all()
        serializer = ServiceCategorySerializer(serviceCategories, many=True)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['GET'])
def service_category_by_id(request, pk):

    try:

        serviceCategory = ServiceCategory.objects.get(pk=pk)
        serializer = ServiceCategorySerializer(serviceCategory, many=False)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)


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

        return generic_data_response(calendar_data)

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def handle_payment(request):

    try:

        auth_user = AuthUser.objects.get(pk=request.user.id)
        work_order = request.data.get('work_order')

        customer = conekta.Customer.create({
            'name': request.data.get('customer')['name'],
            'email': request.data.get('customer')['email'],
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

            return generic_data_response({
                'payment_status': order.payment_status,
                'payment_amount': f'${str((order.amount / 100))} {order.currency}',
                'payment_method': {
                    'brand': order.charges[0].payment_method.brand,
                    'last4': order.charges[0].payment_method.last4,
                }
            })

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def work_orders(request):

    try:

        if request.method == 'GET':

            work_orders = WorkOrder.objects.filter(customer_profile=CustomerProfile.objects.get(auth_user=request.user.id))
            serializer = WorkOrderSerializer(work_orders, many=True)

            return generic_data_response(serializer.data)

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

                        work_order_instance.line_items.add(LineItem.objects.create(
                            service=Service.objects.get(pk=line_item['service_id']),
                            service_date=line_item['service_date'],
                            service_time=line_item['service_time'],
                            quantity=line_item['quantity'],
                            price=line_item['price']
                        ))

                    transaction.savepoint_commit(line_items_savepoint)
                    return generic_data_response(work_order_serializer.data)

                return generic_bad_request()

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def staffing_assignment(request):

    try:

        if request.method == 'GET':
            return generic_data_response({})

        elif request.method == 'POST':

            line_items = WorkOrder.objects.get(pk=request.data.get('work_order_id')).line_items.all()
            staffing_assignments = []

            for line_item in line_items:

                for i in range(1, line_item.quantity + 1):

                    staffing_assignment = StaffingAssigmentSerializer(StaffingAssignment.objects.create(
                        line_item=line_item,
                        index=i
                    ))

                    staffing_assignments.append(staffing_assignment.data)

            return generic_data_response(staffing_assignments)

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def staffing_assignment_beautier(request):

    try:

        if request.method == 'GET':
            return generic_data_response({})

        elif request.method == 'POST':

            staffing_assignments = StaffingAssignment.objects.filter(id__in=request.data.get('staffing_assignment_ids'))
            beautier_profile = BeautierProfile.objects.get(pk=request.data.get('beautier_id'))

            for staffing_assignment in staffing_assignments:
                staffing_assignment.beautier_profiles.add(beautier_profile)

            return generic_data_response({})

    except Exception as err:
        return generic_internal_server_error_response(err)



@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def get_formatted_address(request):

    google_maps_client = googlemaps.Client(key='AIzaSyAP1kEvf4GgsAVLzI2MLGKpi1w17nmNDTQ')

    try:

        response = google_maps_client.place(request.data['place_id'])
        return generic_data_response(response['result']['formatted_address'])

    except Exception as err:
        return generic_internal_server_error_response(err)


"""
ADMIN ENDPOINTS
"""

@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def customer_profiles(request):

    try:

        customer_profiles = CustomerProfile.objects.all()
        customer_profile_serializer = CustomerProfileSerializer(customer_profiles, many=True)

        return generic_data_response(customer_profile_serializer.data);

    except Exception as err:
        return generic_internal_server_error_response(err)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_work_orders(request):

    try:

        work_orders = WorkOrder.objects.all()
        work_orders_serializer = WorkOrderSerializer(work_orders, many=True)

        return generic_data_response(work_orders_serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)
