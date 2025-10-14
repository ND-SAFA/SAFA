import json
from abc import ABC, abstractmethod
from typing import Callable, Dict, Type, Union

from django.http import HttpRequest, JsonResponse

from api.endpoints.auth_view import authorize_request
from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from api.utils.view_util import ViewUtil
from tgen.common.util.json_util import NpEncoder


class IHandler(ABC):
    def __init__(self, func: Callable[[Dict], Dict], serializer: Type[AbstractSerializer], skip_serialization: bool = False):
        """
        Creates endpoint handler with given callable.
        :param func: The function handling incoming request.
        :param serializer: Parses and validates request data.
        :param skip_serialization: Whether to skip during handling of request..
        """
        self.func = func
        self.serializer = serializer
        self.skip_serialization = skip_serialization

    @abstractmethod
    def _request_handler(self, data: Dict) -> Union[JsonResponse, Dict]:
        """
        Handles request with given data.
        :param data: The data from request.
        :return: The endpoint response.
        """

    def handle_request(self, request: HttpRequest) -> JsonResponse:
        """
        Reads request and delegates to child handler. Json Response is returned.
        :param request: The request to handle.
        :return: The response of the endpoint.
        """
        serialized_data, raw_data = ViewUtil.read_request(request, self.serializer)
        error = authorize_request(request, raw_data)
        if error:
            return JsonResponse({'error': str(error)}, status=400)
        if self.skip_serialization:
            serialized_data = json.loads(request.body)  # will re-serialize but make sure serializer passes before starting job

        response = self._request_handler(serialized_data)
        if isinstance(response, JsonResponse):
            return response
        return JsonResponse(response, encoder=NpEncoder, safe=False)

    def serialize_data(self, data: Dict):
        """
        Serializes data given.
        :param data: The data to serialize.
        :return: Validated data.
        """
        s = self.serializer(data=data)
        s.is_valid(raise_exception=True)
        serialized_data = s.save()
        return serialized_data
