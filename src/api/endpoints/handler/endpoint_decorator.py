from typing import Callable

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework.views import APIView

from api.docs.doc_generator import autodoc
from api.endpoints.handler.async_endpoint_handler import AsyncEndpointHandler
from api.endpoints.handler.endpoint_handler import EndpointHandlerProxy
from tgen.common.constants import environment_constants
from tgen.common.util.json_util import NpEncoder

load_dotenv()


def endpoint(serializer, is_async: bool = False):
    """
    Creates endpoint decorator with given configuration.
    :param serializer: The serializer used to read request data.
    :param is_async: Whether the endpoint will be perform a syncronous function.
    :return: The decorator that will take in the endpoint function.
    """

    def dec(func) -> Callable:
        """
        Decorates function with either sync or async endpoint decorator.
        :param func: The function to decorate.
        :return: Reference to decorated endpoint.
        """
        if is_async and not environment_constants.IS_TEST:
            return async_endpoint_decorator(serializer, func)
        return sync_endpoint_decorator(serializer, EndpointHandlerProxy(func, serializer, is_async=is_async))

    return dec


def endpoint_get(func) -> Callable:
    """
    Creates endpoint for GET request.
    :param func: The function to call when get is called.
    :return: Reference to decorated function
    """

    def dec(*args, **kwargs):
        """
        Creates a GET class decorator for function.
        :return: The class decorator
        """
        return class_decorator_get(func)

    return dec


def async_endpoint_decorator(serializer, func):
    """
    Decorates func to be a celery task.
    :param serializer: The serializer used to parse the input data.
    :param func: The executing function.
    :return: Task endpoint handler.
    """
    request_receiver = AsyncEndpointHandler.create_receiver(func, serializer)
    return sync_endpoint_decorator(serializer, request_receiver)


def sync_endpoint_decorator(serializer, func) -> Callable:
    """
    Creates API endpoint for a syncronous endpoint using function to execute a task.
    :param serializer: Serializes request data into func input data.
    :param func: The function to execute a job.
    :return: The endpoint callable.
    """

    class APIDecorator(APIView):
        """
        Internal class supported the auto-generation of endpoint documentation.
        """

        @autodoc(serializer)
        @csrf_exempt
        def post(self, request: HttpRequest):
            """
            The POST method handler logic.
            :param request: The incoming request.
            :return: JSON response.
            """
            return func(request)

    return APIDecorator.as_view()


def class_decorator_get(func):
    """
    Decorates function so that it becomes an GET endpoint.
    :param func: The function returning data.
    :return: GET endpoint using function to retrieve data to send back.
    """

    class APIDecorator(APIView):
        """
        Internal class supported the auto-generation of endpoint documentation.
        """

        @csrf_exempt
        def get(self, request: HttpRequest):
            """
            The POST method handler logic.
            :param request: The incoming request.
            :return: JSON response.
            """
            # TODO: Currently ignoring request, can see this needed for params later.
            response_data = func()
            return JsonResponse(response_data, encoder=NpEncoder, safe=False)

    return APIDecorator.as_view()
