import json
import threading
from typing import Any, Callable, Dict, Type

from celery import shared_task
from django.http import JsonResponse

from api.constants.config import get_current_version
from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.handler.ihandler import IHandler
from gen_common.infra.t_logging.log_capture import LogCapture
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.traceability.relationship_manager.model_cache import ModelCache

from gen_common.util.json_util import NpEncoder



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

    def _request_handler(self, data: Dict) -> JsonResponse:
        """
        Processes data through a celery task.
        :param data: The request data.
        :return: None
        """
        result = self.task.delay(data)
        task_id = result.id
        return JsonResponse({"task_id": task_id}, encoder=NpEncoder)

    def create_task(self):
        """
        :return: reference to celery task function.
        """

        @shared_task(name=self.func.__name__)
        def task(data):
            """
            The Celery task responsible for starting job, polling / publishing logs, and saving job output.
            :param data: The input data to the job.
            :return:
            """
            self.is_running = True
            self.pre_process()
            self.poll_job(data)
            self.post_process()
            if self.exception:
                raise self.exception
            return self.result["output"]

        return task

    def poll_job(self, data) -> None:
        """
        Runs the job within a thread using the main thread to update the task logs.
        :param data: The input data to the job.
        :return: None
        """
        thread = threading.Thread(target=self.run_job, args=[data])
        thread.start()
        while self.is_running:
            self.write_logs()
            threading.Event().wait(5)
        thread.join()

    def run_job(self, data: Dict) -> None:
        """
        Executes job on data. Serializes input data, runs function on data, and stores output.
        :param data: The input data to the job.
        :return: None
        """
        try:
            logger.info(f"Welcome to GEN @ {get_current_version()}")
            ModelCache.clear()
            data = self.serialize_data(data)
            response = self.func(data)
            response_dict = self.encode_object(response)
            self.result["output"] = response_dict
            self.is_success = True
        except Exception as e:
            logger.exception(e)
            self.is_success = False
            self.exception = e
        ModelCache.clear()
        self.is_running = False

    def pre_process(self) -> None:
        """
        Creates log capture.
        :return: None
        """
        self.log_capture = LogCapture()
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
    def create_receiver(func, serializer):
        """
        Creates reference to request handler for a function to perform asyncronously.
        :param func: The function to perform.
        :param serializer: The serializer to preprocess input data with.
        :return: Reference to request handler.
        """
        handler = AsyncEndpointHandler(func, serializer)
        return lambda r: handler.handle_request(r)

    @staticmethod
    def encode_object(response: Any) -> Dict:
        """
        Dumps JobOutput into JSON then reloads it so that final content is guranteed to be serializable.
        :param response: The response to encode into JSON.
        :return: Response dictionary.
        """
        response_str = json.dumps(response, cls=NpEncoder)
        response_dict = json.loads(response_str)
        return response_dict


def remove_handlers(logger) -> None:
    """
    Removes logger handlers.
    :param logger: The logger to remove handlers from.
    :return: None
    """
    for handler in logger.handlers:
        logger.removeHandler(handler)
