from typing import Dict

from server.api import RequestParams
from django.http.request import HttpRequest
from django.http.response import JsonResponse

from jobs.common.arg_builder import build_trace_args
from jobs.common.job_type import JobType


def predict(request: HttpRequest) -> JsonResponse:
    return _run_job(request, JobType.PREDICT)


def fine_tune(request: HttpRequest) -> JsonResponse:
    return _run_job(request, JobType.TRAIN)


def _run_job(request, job_type):
    args = _make_job_params_from_request(request.POST)
    job = job_type.value(args)
    job_results = job.start()
    return _as_json(job_results)


def _make_job_params_from_request(params: Dict):
    model_path = params[RequestParams.MODEL_PATH]
    sources = params[RequestParams.SOURCES]
    targets = params[RequestParams.TARGETS]
    base_model = params[RequestParams.BASE_MODEL]
    links = params.get(RequestParams.LINKS, None)
    output_path = params.get(RequestParams.OUTPUT_PATH, None)
    return build_trace_args(base_model, links, model_path, output_path, sources, targets)


def _as_json(response_object: Dict) -> JsonResponse:
    return JsonResponse(response_object, safe=False)
