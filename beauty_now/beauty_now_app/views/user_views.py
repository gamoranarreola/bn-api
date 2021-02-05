from requests.api import post
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib3.util.url import get_host

from ..models.user_models import CustomUser
from ..serializers.user_serializers import MeSerializer
from beauty_now_utils.responses.generic_responses import generic_data_response, generic_internal_server_error_response


class UserActivationView(APIView):
    """[summary]

    Arguments:
        APIView {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    def get (self, request, uid, token):
        """[summary]

        Arguments:
            request {[type]} -- [description]
            uid {[type]} -- [description]
            token {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
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

    except:

        return generic_internal_server_error_response()
