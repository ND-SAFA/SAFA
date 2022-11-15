from typing import Dict, Union

from drf_yasg.openapi import Schema, TYPE_OBJECT
from rest_framework import permissions, status
from rest_framework.views import APIView

from api.responses.base_response import BaseResponse


class AbstractTraceView(APIView):
    permission_classes = (permissions.AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_responses(response_keys: Union[str, list]) -> Dict:
        """
        Gets properties used to generate response documentation
        :param response_keys: either a single response key or a list of response keys to get properties for
        :return: the response dictionary
        """
        return {
            status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                                       properties=BaseResponse.get_properties(response_keys))}
