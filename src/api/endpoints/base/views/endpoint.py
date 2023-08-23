import json
import threading
from typing import Any, Callable, Dict, Optional

from celery import Task, shared_task
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from api.endpoints.base.docs.doc_generator import autodoc
from api.utils.view_util import ViewUtil
from tgen.common.util.json_util import NpEncoder
from tgen.common.util.logging.log_capture import LogCapture
from tgen.common.util.logging.logger_manager import logger


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


def async_endpoint(serializer, pre_process: PreProcessType = None, post_process: PostProcessType = None):
    """
    Publishes function as an endpoint run as a celery task.
    :param serializer: The endpoint serializer.
    :param post_process: The function used for post-processing result with pre-processing state.
    :return: Decorator creating endpoint and celery task.
    """
    pre_process = [pre_process] if pre_process else []
    post_process = [post_process] if post_process else []

    def decorator(func=None, *args, **kwargs):
        """
        Decorates function as endpoint run as celery task.
        :param func: The function to run as celery task.
        :param args: Positional arguments for constructing task.
        :param kwargs: Additional keyword arguments constructing task.
        :return: Wrapped function.
        """

        @endpoint(serializer)
        @shared_task(*args, **kwargs, name=func.__name__, bind=True)
        def task_endpoint(self: Task, *task_args, **task_kwargs):
            """
            Constructs an task endpoint who will queue a job performing function being wrapped.
            :param task_args: Positional arguments.
            :param task_kwargs: Keyword arguments.
            :return: JsonResponse containing function output as body.
            """
            local_state = endpoint_preprocess()

            for p in pre_process:
                p_state = p(*task_args, **task_kwargs)
                assert isinstance(p_state, dict), "Expected pre-processing output to be a dictionary."
                local_state.update(p_state)

            result = {}
            local_state["is_running"] = True
            local_state["success"] = True

            def write_logs():
                log_capture = local_state["log_capture"]
                is_successful = local_state["success"]
                if not is_successful:
                    raise local_state["exception"]
                logs = log_capture.get_logs()
                self.update_state(state="PROGRESS", meta={'logs': logs})

            def run_job():
                try:
                    data, *other_args = task_args
                    s = serializer(data=data)
                    s.is_valid(raise_exception=True)
                    serialized_data = s.save()
                    response = func(serialized_data, *other_args, **task_kwargs)
                    response_str = json.dumps(response, cls=NpEncoder)
                    response_dict = json.loads(response_str)
                    result.update(response_dict)
                    local_state["is_running"] = False
                except Exception as e:
                    logger.exception(e)
                    local_state["is_running"] = False
                    local_state["success"] = False
                    local_state["exception"] = e

            thread = threading.Thread(target=run_job)
            thread.start()

            while local_state["is_running"]:
                write_logs()
                threading.Event().wait(5)
            thread.join()

            endpoint_postprocess(local_state, result)
            for post in post_process:
                post(local_state, result)

            write_logs()
            logger.info("Exiting. Bye Bye.")
            return result

        assert func is not None, "Expected function to be defined."
        return task_endpoint

    return decorator


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
