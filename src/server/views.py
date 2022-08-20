from typing import Dict

from server.api import Api
from django.http.request import HttpRequest
from django.http.response import JsonResponse

from trace.config.constants import VALIDATION_PERCENTAGE_DEFAULT
from trace.jobs.trace_args_builder import TraceArgsBuilder
from server.job_type import JobType


def predict(request: HttpRequest) -> JsonResponse:
    return _run_job(request, JobType.PREDICT)


def fine_tune(request: HttpRequest) -> JsonResponse:
    return _run_job(request, JobType.TRAIN)


def _run_job(request, job_type):
    args = _make_job_params_from_request(request.POST)
    job = job_type.value(args)
    job_results = job.start()
    return _as_json(job_results.output)


def _make_job_params_from_request(params: Dict):
    model_path = params[Api.MODEL_PATH]
    sources = params[Api.SOURCES]
    targets = params[Api.TARGETS]
    base_model = params[Api.BASE_MODEL]
    links = params.get(Api.LINKS, None)
    output_path = params.get(Api.OUTPUT_PATH, None)
    kwargs = params.get(Api.SETTINGS)
    return TraceArgsBuilder(base_model, model_path, output_path, sources, targets, links, VALIDATION_PERCENTAGE_DEFAULT,
                            prediction_ids_key=Api.PREDICTION_IDS, **kwargs)


def _as_json(response_object: Dict) -> JsonResponse:
    return JsonResponse(response_object, safe=False)
