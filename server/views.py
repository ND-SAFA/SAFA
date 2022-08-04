from typing import Dict

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from api import RequestParams
from jobs.fine_tune.model_fine_tune_args import ModelFineTuneArgs
from jobs.abstract.job_type import JobType


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
    return ModelFineTuneArgs(base_model=base_model, model_path=model_path, output_path=output_path,
                             s_arts=sources, t_arts=targets, links=links)


def _as_json(response_object: Dict) -> JsonResponse:
    return JsonResponse(response_object, safe=False)
