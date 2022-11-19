from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


def response_200(data):

    return Response({"data": data, "status": HTTP_200_OK})


def response_201(data):

    return Response({"data": data, "status": HTTP_201_CREATED})


def response_204(data):

    return Response({"data": data, "status": HTTP_204_NO_CONTENT})


def response_400(data):

    return Response({"data": data, "status": HTTP_400_BAD_REQUEST})


def response_500(err):

    return Response(
        {
            "data": {
                "message": "Ha ocurrido un error en el servidor.",
                "error": f"{err}",
            },
            "status": HTTP_500_INTERNAL_SERVER_ERROR,
        }
    )
