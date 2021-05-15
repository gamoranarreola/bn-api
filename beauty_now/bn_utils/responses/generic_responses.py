from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR


def generic_data_response(data):

    return Response({
        'data': data,
        'status': HTTP_200_OK
    })

def generic_internal_server_error_response(err):

    return Response({
        'data': {
            'message': 'Ha ocurrido un error en el servidor.',
            'error': f'{err}'
        },
        'status': HTTP_500_INTERNAL_SERVER_ERROR
    })
