from celery import Task
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from api.endpoints.base.docs.doc_generator import autodoc
from api.utils.view_util import ViewUtil


def endpoint(serializer):
    """
    Decorator for creating automatic documentation, serialization, and job handling.
    :param serializer: The serializer to use for parsing payload.
    :return: Handler function accepting `POST` method.
    """
    if serializer is None:
        raise Exception("Endpoint requires serializer to parse request.")

    def decorator(func: Task):
        """
        Decorates task function in API view for POST request.
        :param func: The function to handle the payload of request.
        :return: View wrapped function.
        """

        class APIDecorator(APIView):
            """
            Internal class supported the autogeneration of endpoint documentation.
            """

            @autodoc(serializer)
            @csrf_exempt
            def post(self, request: HttpRequest):
                """
                The POST method handler logic.
                :param request: The incoming request.
                :return: JSON response.
                """
                assert request.method == 'POST', "Only POST accepted for request."
                payload = ViewUtil.read_request(request, serializer)
                if isinstance(func, Task):
                    task = func.delay(payload)
                    return JsonResponse({"task_id": task.id})
                else:
                    response = func(payload)
                    if isinstance(response, JsonResponse):
                        return response
                    return JsonResponse(response)

        return APIDecorator.as_view()

    return decorator
