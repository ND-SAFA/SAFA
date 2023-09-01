import json
import threading
from typing import Type

from celery import Task, shared_task
from rest_framework import serializers

from api.constants.config import get_api_header
from api.endpoints.base.endpoint import PostProcessType, PreProcessType, endpoint, endpoint_postprocess, endpoint_preprocess
from tgen.common.util.json_util import NpEncoder
from tgen.common.util.logging.logger_manager import logger


def async_endpoint(serializer: Type[serializers.Serializer], pre_process: PreProcessType = None, post_process: PostProcessType = None):
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

        @endpoint(serializer, skip_serialization=True)
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
                    logger.info(get_api_header())
                    data, *other_args = task_args
                    s = serializer(data=data)
                    s.is_valid(raise_exception=True)
                    data = s.save()
                    response = func(data, *other_args, **task_kwargs)
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
