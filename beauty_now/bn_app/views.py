from requests.api import post
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
import googlemaps
import conekta

conekta.api_key = 'key_qrXw7xpD26Czohm81ErhrA'
conekta.locale = 'es'
conekta.api_version = "2.5.1"

from beauty_now.bn_utils.google.google import *

from beauty_now.bn_app.models import (
    CustomUser,
    BeautierProfile,
    Service,
    ServiceCategory,
    CustomerProfile,
    CustomerProfileAddress,
    WorkOrder
)

from beauty_now.bn_app.serializers import (
    MeSerializer,
    BeautierProfileSerializer,
    ServiceSerializer,
    ServiceCategorySerializer,
    WorkOrderSerializer,
    CustomerProfileAddressSerializer
)

from beauty_now.bn_utils.responses.generic_responses import (
    generic_data_response,
    generic_internal_server_error_response
)

from beauty_now.bn_core.tasks import handle_initial_work_order_request


class UserActivationView(APIView):

    def get(self, request, uid, token):

        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + '/api/auth/users/activation/'
        post_data = {'uid': uid, 'token': token}
        result = post(post_url, data=post_data)

        return Response(result.status_code)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):

    try:

        custom_user = CustomUser.objects.get(pk=request.user.id)
        serializer = MeSerializer(custom_user, many=False)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)

@api_view(['GET'])
def beautiers(request):

    try:

        beautiers = BeautierProfile.objects.all()
        serializer = BeautierProfileSerializer(beautiers, many=True)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)

@api_view(['GET'])
def beautier_by_id(request, pk):

    try:

        beautier = BeautierProfile.objects.get(pk=pk)
        serializer = BeautierProfileSerializer(beautier, many=False)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)

@api_view(['POST'])
def beautiers_for_specialties(request):

    try:

        beautiers_for_specialties = BeautierProfile.objects.filter(beautierprofilespecialty__specialty__in=request.data['specialty_ids']).distinct()
        serializer = BeautierProfileSerializer(beautiers_for_specialties, many=True)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)

@api_view(['GET'])
def service_by_id(request, pk):

    try:

        service = Service.objects.get(pk=pk)
        serializer = ServiceSerializer(service, many=False)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)

@api_view(['GET'])
def service_by_category_id(request, service_category_id):

    try:

        services = Service.objects.filter(category_id=service_category_id)
        serializer = ServiceSerializer(services, many=True)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)

@api_view(['GET'])
def service_categories(request):

    try:

        serviceCategories = ServiceCategory.objects.all()
        serializer = ServiceCategorySerializer(serviceCategories, many=True)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)

@api_view(['GET'])
def service_category_by_id(request, pk):

    try:

        serviceCategory = ServiceCategory.objects.get(pk=pk)
        serializer = ServiceCategorySerializer(serviceCategory, many=False)

        return generic_data_response(serializer.data)

    except Exception as err:
        return generic_internal_server_error_response(err)

@api_view(['POST'])
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

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def send_email(request):

    try:
        send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['to@doradoaguilusjoel@gmail.com'],
            fail_silently=False,
        )
        return generic_data_response({'test':'ok'})

    except Exception as err:
        return generic_internal_server_error_response(err)

def create_work_order_instance(work_order_data, custom_user_id):

    data = {
        'request_date': work_order_data.get('request_date'),
        'request_time': work_order_data.get('request_time'),
        'customer_profile': CustomerProfile.objects.get(custom_user=custom_user_id).id,
        'place_id': work_order_data.get('place_id'),
        'notes': work_order_data.get('notes'),
        'line_items': work_order_data.get('line_items'),
        'status': work_order_data.get('status')
    }

    work_order_serializer = WorkOrderSerializer(data=data)

    if work_order_serializer.is_valid():

        work_order_instance = work_order_serializer.save()

        return {
            'instance': work_order_instance,
            'serializer': work_order_serializer
        }

def create_customer_profile_address(place_id, custom_user_id):

    if not CustomerProfileAddress.objects.filter(customer_profile=CustomerProfile.objects.get(custom_user=custom_user_id)).filter(place_id=place_id).exists():

        customer_profile_address_serializer = CustomerProfileAddressSerializer(data={
            'customer_profile': CustomerProfile.objects.get(custom_user=custom_user_id).id,
            'place_id': place_id
        })

        if customer_profile_address_serializer.is_valid():

            customer_profile_address_serializer.save()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_payment(request):

    try:

        work_order = request.data.get('work_order')
        total_price = 0

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
            work_order = create_work_order_instance(request.data.get('work_order'), request.user.id)

            if work_order.get('instance') and work_order.get('serializer'):
                create_customer_profile_address(work_order['place_id'], request.user.id)

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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def work_orders(request):

    try:

        if request.method == 'GET':

            work_orders = WorkOrder.objects.filter(customer_profile=CustomerProfile.objects.get(custom_user=request.user.id))
            serializer = WorkOrderSerializer(work_orders, many=True)

            return generic_data_response(serializer.data)

        elif request.method == 'POST':

            work_order = create_work_order_instance(request.data.get('work_order'), request.user.id)

            if work_order.get('instance') and work_order.get('serializer'):

                create_customer_profile_address(request.data.get('work_order')['place_id'], request.user.id)

            handle_initial_work_order_request.delay(request.user.id, request.data.get('work_order'), request.data.get('formatted_address'))

            return generic_data_response(work_order.get('serializer').data)

    except Exception as err:
        return generic_internal_server_error_response(err)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_formatted_address(request):

    google_maps_client = googlemaps.Client(key='AIzaSyAP1kEvf4GgsAVLzI2MLGKpi1w17nmNDTQ')

    try:

        response = google_maps_client.place(request.data['place_id'])
        return generic_data_response(response['result']['formatted_address'])

    except Exception as err:
        return generic_internal_server_error_response(err)