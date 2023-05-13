from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.endpoints.base.docs.doc_generator import autodoc
from api.utils.view_util import ViewUtil
from tgen.jobs.abstract_job import AbstractJob
from tgen.util.json_util import NpEncoder
from tgen.util.status import Status


def endpoint(serializer):
    def method_handler(method, **kwargs):
        @autodoc(serializer)
        @csrf_exempt
        def request_handler(self, request, **kwargs):
            prediction_payload = ViewUtil.read_request(request, serializer)
            job_tuple = method(self, prediction_payload)
            job: AbstractJob = job_tuple[0]
            post_processor = job_tuple[1]

            def job_handler():
                job_result = job.run()
                job_dict = job_result.to_json(as_dict=True)
                if job_result.status == Status.FAILURE:
                    return JsonResponse(job_dict, status=400)
                return job_dict["body"]

            job_runnable = job if callable(job) else lambda: job_handler()
            response_body = job_runnable()
            response_processed = post_processor(response_body)
            return JsonResponse(response_processed, encoder=NpEncoder)

        return request_handler

    return method_handler
