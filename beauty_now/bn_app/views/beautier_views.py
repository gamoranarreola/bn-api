from rest_framework.compat import distinct
from rest_framework.decorators import api_view

from ..models.beautier_models import BeautierProfile
from ..serializers.beautier_serializers import BeautierProfileSerializer
from bn_utils.responses.generic_responses import generic_data_response, generic_internal_server_error_response


@api_view(['GET'])
def beautiers(request):

    try:

        beautiers = BeautierProfile.objects.all()
        serializer = BeautierProfileSerializer(beautiers, many=True)

        return generic_data_response(serializer.data)

    except:

        return generic_internal_server_error_response()


@api_view(['GET'])
def beautier_by_id(request, pk):

    try:

        beautier = BeautierProfile.objects.get(pk=pk)
        serializer = BeautierProfileSerializer(beautier, many=False)

        return generic_data_response(serializer.data)

    except:

        return generic_internal_server_error_response()


@api_view(['POST'])
def beautiers_for_specialties(request):

    try:

        beautiers_for_specialties = BeautierProfile.objects.filter(beautierprofilespecialty__specialty__in=request.data['specialty_ids']).distinct()
        serializer = BeautierProfileSerializer(beautiers_for_specialties, many=True)

        return generic_data_response(serializer.data)

    except:

        return generic_internal_server_error_response()
