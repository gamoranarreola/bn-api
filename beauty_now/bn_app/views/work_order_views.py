import googlemaps
import conekta
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from bn_core.tasks import handle_initial_work_order_request
from bn_utils.responses.generic_responses import generic_data_response, generic_internal_server_error_response
from ..models.customer_profile_models import CustomerProfile, CustomerProfileAddress
from ..models.work_order_models import WorkOrder
from ..serializers.user_serializers import CustomerProfileAddressSerializer
from ..serializers.work_order_serializers import WorkOrderSerializer

conekta = {}

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

    except:

        return generic_internal_server_error_response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment(request):

    conekta.api_key = 'key_qrXw7xpD26Czohm81ErhrA'
    conekta.locale = 'es'

    try:

        token = request.data.get('token')
        line_items = []
        total_price = 0

        for item in request.data.get('workOrders'):

            service = item['service']
            category = service['category']
            total_price += (service['public_price'] * item['items'] )*100

            line_items.append({
                "name": service['name'],
                "description": 'Description:' + service['description'],
                "unit_price": service['public_price']*100,
                "quantity": item['items'],
                "sku": service['service_id'],
                "category":category['name'],
            })

        order = conekta.Order.create({
            "line_items": line_items,
            "customer_info":{
                "name": request.data.get('name') ,
                "phone": request.data.get('phone') ,
                "email": request.data.get('email') ,
                "corporate": False,
                "vertical_info": {}
            },
            "charges": [{
                "payment_method":{
                "type": "card",
                "token_id": token
                },
                "amount": total_price
            }],
            "currency" : "mxn",
        })

        if order.payment_status == 'paid':

            for workOrder in request.data.get('workOrders'):

                work_order = create_work_order_instance(workOrder['workOrder']['work_order'], request.user.id)

                if work_order.get('instance') and work_order.get('serializer'):

                    create_customer_profile_address(workOrder['workOrder']['work_order']['place_id'], request.user.id)

        return generic_data_response(order.payment_status)

    except conekta.ConektaError as e:
        print(e.message)
        return generic_internal_server_error_response()


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

    except:

        return generic_internal_server_error_response()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_formatted_address(request):

    google_maps_client = googlemaps.Client(key='AIzaSyCs_oCa_PkCvSPDbNttUCIyK6_BWbvO008')

    try:

        response = google_maps_client.place(request.data['place_id'])

        return generic_data_response(response['result']['formatted_address'])

    except:

        return generic_internal_server_error_response()


def create_work_order_instance(work_order_data, custom_user_id):

    data = {
        'request_date': work_order_data.get('request_date'),
        'request_time': work_order_data.get('request_time'),
        'customer_profile': CustomerProfile.objects.get(custom_user=custom_user_id).id,
        'place_id': work_order_data.get('place_id'),
        'notes': work_order_data.get('notes'),
        'line_items': work_order_data.get('line_items')
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
