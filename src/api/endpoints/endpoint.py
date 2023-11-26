import json
from typing import Any, Callable, Dict, Optional

from celery import Task
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from api.docs.doc_generator import autodoc
from api.utils.view_util import ViewUtil
from tgen.common.logging.log_capture import LogCapture
from tgen.common.logging.logger_manager import logger
from tgen.common.util.json_util import NpEncoder


def endpoint(serializer, skip_serialization: bool = False):
    """
    Decorator for creating automatic documentation, serialization, and job handling.
    :param serializer: The serializer to use for parsing payload.
    :param skip_serialization: Skip serialization.
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
                assert request.method == 'POST', "Only POST accepted for request."
                if skip_serialization:
                    payload = json.loads(request.body)
                else:
                    payload = ViewUtil.read_request(request, serializer)

                if isinstance(func, Task):
                    payload_str = json.dumps(payload, cls=NpEncoder)
                    payload_dict = json.loads(payload_str)
                    task = func.delay(payload_dict)
                    return JsonResponse({"task_id": task.id}, encoder=NpEncoder)
                else:
                    response = func(payload)
                    if isinstance(response, JsonResponse):
                        return response
                    return JsonResponse(response, encoder=NpEncoder, safe=False)

        return APIDecorator.as_view()

    return decorator


PreProcessType = Callable[[Any], Optional[Dict]]
PostProcessType = Callable[[Dict, Dict], None]


def endpoint_preprocess():
    log_capture = LogCapture()

    def remove_handlers(logger):
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    remove_handlers(logger)
    log_capture.clear()
    return {"log_capture": log_capture}


def endpoint_postprocess(state, result):
    log_capture = state["log_capture"]
    log_capture.clear()
    result["logs"] = log_capture.get_logs()
