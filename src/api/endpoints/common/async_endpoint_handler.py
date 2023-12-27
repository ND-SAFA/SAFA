import json
import threading
from typing import Any, Callable, Dict, Type

from celery import shared_task
from django.http import JsonResponse

from api.endpoints.common.ihandler import IHandler
from api.endpoints.serializers.abstract_serializer import AbstractSerializer
from tgen.common.logging.log_capture import LogCapture
from tgen.common.logging.logger_manager import logger
from tgen.common.util.json_util import NpEncoder
from tgen.embeddings.model_cache import ModelCache
from tgen.models.llm.anthropic_manager import get_client


class AsyncEndpointHandler(IHandler):

    def __init__(self, func: Callable, serializer: Type[AbstractSerializer]):
        """
        Constructs async endpoint handler.
        :param func: The function to run within a celery task.
        :param serializer: The serializer responsible for reading request data.
        """
        super().__init__(func, serializer, skip_serialization=True)
        self.is_running = False
        self.is_success = True
        self.log_capture = None
        self.exception = None
        self.task = None
        self.result = {}
        self.task = self.create_task()

    @staticmethod
    def create_receiver(func, serializer):
        handler = AsyncEndpointHandler(func, serializer)
        return lambda r: handler.handle_request(r)

    def _request_handler(self, data: Dict) -> JsonResponse:
        """
        Processes data through a celery task.
        :param data: The request data.
        :return: None
        """
        result = self.task.delay(data)
        return JsonResponse({"task_id": result.id}, encoder=NpEncoder)

    def create_task(self):
        @shared_task(name=self.func.__name__)
        def task(data):
            self.is_running = True
            self.pre_process()
            self.poll_job(data)
            self.post_process()
            return self.result["output"]

        return task

    def poll_job(self, data) -> None:
        """
        Runs the job within a thread using the main thread to update the task logs.
        :return: None
        """
        thread = threading.Thread(target=self.run_job, args=[data])
        thread.start()
        while self.is_running:
            self.write_logs()
            threading.Event().wait(5)
        thread.join()

    def run_job(self, data):
        """
        Runs the
        :return:
        """
        try:
            ModelCache.clear()
            get_client(refresh=True)
            data = self.serialize_data(data)
            response = self.func(data)
            response_dict = self.encode_object(response)
            self.result["output"] = response_dict
            self.is_success = True
        except Exception as e:
            logger.exception(e)
            self.is_success = False
            self.exception = e
        self.is_running = False

    def pre_process(self):
        """
        Creates log capture.
        :return: None
        """
        self.log_capture = LogCapture()

        def remove_handlers(logger):
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

        remove_handlers(logger)
        self.log_capture.clear()

    def post_process(self) -> None:
        """
        Uploads final task logs and clears the capture.
        :return:None
        """
        self.result["logs"] = self.log_capture.get_logs()
        self.log_capture.clear()

    def write_logs(self) -> None:
        """
        Writes current log to the task meta.
        :return:None
        """
        if not self.is_success:
            raise self.exception
        logs = self.log_capture.get_logs()
        self.task.update_state(state="PROGRESS", meta={'logs': logs})

    @staticmethod
    def encode_object(response: Any):
        response_str = json.dumps(response, cls=NpEncoder)
        response_dict = json.loads(response_str)
        return response_dict
