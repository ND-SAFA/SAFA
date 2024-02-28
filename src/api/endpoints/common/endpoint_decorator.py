from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework.views import APIView

from api.docs.doc_generator import autodoc
from api.endpoints.common.async_endpoint_handler import AsyncEndpointHandler
from api.endpoints.common.endpoint_handler import EndpointHandlerProxy
from tgen.common.constants import environment_constants

load_dotenv()


def endpoint(serializer, is_async: bool = False):
    """
    Creates endpoint decorator with given configuration.
    :param serializer: The serializer used to read request data.
    :param is_async: Whether the endpoint will be perform a syncronous function.
    :return: The decorator that will take in the endpoint function.
    """

    def dec(func):
        if is_async and not environment_constants.IS_TEST:
            return create_task_decorator(serializer, func)
        return class_decorator(serializer, EndpointHandlerProxy(func, serializer, is_async=is_async))

    return dec


def endpoint_get(func):
    """
    Creates endpoint for GET request.
    :param func: The function to call when get is called.
    :return:
    """

    def dec(*args, **kwargs):
        return class_decorator_get(func)

    return dec


def create_task_decorator(serializer, func):
    """
    Decorates func to be a celery task.
    :param serializer: The serializer used to parse the input data.
    :param func: The executing function.
    :return: Task endpoint handler.
    """
    request_receiver = AsyncEndpointHandler.create_receiver(func, serializer)
    return class_decorator(serializer, request_receiver)


def class_decorator(serializer, func):
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
            return func()

    return APIDecorator.as_view()
