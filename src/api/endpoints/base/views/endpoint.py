from typing import Tuple

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.endpoints.base.docs.doc_generator import autodoc
from api.utils.view_util import ViewUtil
from tgen.jobs.abstract_job import AbstractJob
from tgen.util.json_util import NpEncoder
from tgen.util.status import Status


def endpoint(serializer):
    """
    Decorator for creating automatic documentation, serialization, and job handling.
    :param serializer: The serializer to use for parsing payload.
    :return: Handler function accepting `POST` method.
    """
    if serializer is None:
        raise Exception("Endpoint requires serializer to parse request.")

    def method_handler(endpoint_method):
        """
        Decorator for performing endpoint method alongside auto documenting it and job handling.
        :param endpoint_method: The method performing endpoint logic.
        :return: Request handler
        """

        @autodoc(serializer)
        @csrf_exempt
        def request_handler(method_class_instance, request):
            """
            Decorator serializing request and performing job handling.
            :param method_class_instance: The instance of the class encapsulating method (`self`).
            :param request: The request containing payload.
            :return: Endpoint response containing error if occurred or job result if successful.
            """
            prediction_payload = ViewUtil.read_request(request, serializer)
            job_tuple = endpoint_method(method_class_instance, prediction_payload)
            if isinstance(job_tuple, Tuple):
                job: AbstractJob = job_tuple[0]
                post_processor = job_tuple[1]
            else:
                job = job_tuple
                post_processor = lambda p: p

            def job_handler():
                """
                Runs jobs and returns body if successful.y
                :return: Error if failure occurs, job result otherwise.
                """
                job_result = job.run()
                job_dict = job_result.to_json(as_dict=True)
                if job_result.status == Status.FAILURE:
                    return JsonResponse(job_dict, status=400)
                return job_dict["body"]

            job_runnable = job if callable(job) else lambda: job_handler()
            response_body = job_runnable()
            if isinstance(response_body, JsonResponse):
                return response_body
            response_processed = post_processor(response_body)
            return JsonResponse(response_processed, encoder=NpEncoder)

        return request_handler

    return method_handler
