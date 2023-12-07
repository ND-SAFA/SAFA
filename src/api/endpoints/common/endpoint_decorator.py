from celery import shared_task
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework.views import APIView

from api.docs.doc_generator import autodoc
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


def create_task_decorator(serializer, func):
    @shared_task(name=func.__name__)
    def task_decorator():
        return class_decorator(serializer, func)

    return task_decorator()


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
