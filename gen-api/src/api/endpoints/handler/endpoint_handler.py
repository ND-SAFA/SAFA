from typing import Any, Callable, Type

from django.http import HttpRequest

from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.handler.async_endpoint_handler import AsyncEndpointHandler
from api.endpoints.handler.ihandler import IHandler
from api.endpoints.handler.sync_endpoint_handler import SyncEndpointHandler
from gen_common.constants import environment_constants


class EndpointHandlerProxy:
    def __init__(self, func: Callable, serializer: Type[AbstractSerializer], is_async: bool):
        """
        Creates endpoint for given callable using serializer to encode the request.
        :param func: The function handling the request.
        :param serializer: The serializer responsible for reading data from request.
        :param is_async: Whether this should run as a job.
        """
        self.is_async = is_async
        self.serializer: Type[AbstractSerializer] = serializer
        self.func = func

    def __call__(self, request: HttpRequest) -> Any:
        """
        Creates and calls endpoint handler with given data.
        :param request: The data to pass to handler.
        :return: The response of the handler.
        """
        handler_class = self._get_handler()
        handler = handler_class(func=self.func, serializer=self.serializer)
        return handler.handle_request(request)

    def _get_handler(self) -> Type[IHandler]:
        """
        :return: Endpoint handler class for current state.
        """
        if self.is_async and not environment_constants.IS_TEST:
            return AsyncEndpointHandler
        else:
            return SyncEndpointHandler
