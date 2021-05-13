import datetime
import os.path
import pickle

import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from oauthlib.oauth2.rfc6749.grant_types import refresh_token
from rest_framework.decorators import api_view

from ..models.service_models import Service, ServiceCategory
from ..models.customer_profile_models import CustomerProfile, CustomerProfileAddress
from ..serializers.service_serializers import ServiceCategorySerializer, ServiceSerializer
from ..serializers.user_serializers import CustomerProfileAddressSerializer
from bn_utils.responses.generic_responses import generic_data_response, generic_internal_server_error_response


@api_view(['GET'])
def service_by_id(request, pk):

    try:

        service = Service.objects.get(pk=pk)
        serializer = ServiceSerializer(service, many=False)

        return generic_data_response(serializer.data)

    except:

        return generic_internal_server_error_response()


@api_view(['GET'])
def service_by_category_id(request, service_category_id):

    try:

        services = Service.objects.filter(category_id=service_category_id)
        serializer = ServiceSerializer(services, many=True)

        return generic_data_response(serializer.data)

    except:

        return generic_internal_server_error_response()


@api_view(['GET'])
def service_categories(request):

    try:

        serviceCategories = ServiceCategory.objects.all()
        serializer = ServiceCategorySerializer(serviceCategories, many=True)

        return generic_data_response(serializer.data)

    except:

        return generic_internal_server_error_response()


@api_view(['GET'])
def service_category_by_id(request, pk):

    try:

        serviceCategory = ServiceCategory.objects.get(pk=pk)
        serializer = ServiceCategorySerializer(serviceCategory, many=False)

        return generic_data_response(serializer.data)

    except:

        return generic_internal_server_error_response()


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

    except:

        return generic_internal_server_error_response()


def get_calendar_service():

    BASE_DIR = os.path.join(os.path.dirname(__file__), '../..')
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    creds = None

    if os.path.exists(BASE_DIR + '/bn_utils/google/token.pickle'):
        with open(BASE_DIR + '/bn_utils/google/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(BASE_DIR + '/bn_app/google/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def handle_calendar_params(calendar):

    return {
        'id': calendar['id'],
        'beautier_name': calendar['summary']
    }


def handle_free_busy_data(free_busy, calendar_id):

    return {
        'time_min': free_busy['timeMin'],
        'time_max': free_busy['timeMax'],
        'busy': free_busy['calendars'][calendar_id]['busy']
    }


def handle_events_data(events):

    formatted_events = []

    for item in events['items']:

        formatted_events.append({
            'id': item['id'],
            'service_name': item['summary'],
            'start': item['start']['dateTime'],
            'end': item['end']['dateTime']
        })

    return formatted_events
