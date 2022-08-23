from typing import Dict

from server.api import Api
from django.http.request import HttpRequest
from django.http.response import JsonResponse

from trace.config.constants import VALIDATION_PERCENTAGE_DEFAULT
from trace.jobs.trace_args_builder import TraceArgsBuilder
from server.job_type import JobType
import json


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
    model_path = params.pop(Api.MODEL_PATH.value)
    sources = params.pop(Api.SOURCES.value)
    targets = params.pop(Api.TARGETS.value)
    base_model = params.pop(Api.BASE_MODEL.value)
    links = _safe_pop(params, Api.LINKS.value)
    output_path = _safe_pop(params, Api.OUTPUT_PATH.value)
    return TraceArgsBuilder(base_model, model_path, output_path, sources, targets, links, VALIDATION_PERCENTAGE_DEFAULT,
                            prediction_ids_key=Api.PREDICTION_IDS, **params)


def _safe_pop(dict_: Dict, key: any, default: any = None):
    return dict_.pop(key) if key in dict_ else default


def _as_json(response_object: Dict) -> JsonResponse:
    return JsonResponse(response_object, safe=False)
