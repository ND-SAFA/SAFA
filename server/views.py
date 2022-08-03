from typing import Dict

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from api import RequestParams
from jobs.fine_tune.model_fine_tune_args import ModelFineTuneArgs


def predict(request: HttpRequest) -> HttpResponse:
    params = request.POST


def fine_tune(request: HttpRequest) -> HttpResponse:
    params = request.POST

    output_path = params[RequestParams.OUTPUT_PATH]


def _make_job_params_from_request(params: Dict):
    model_path = params[RequestParams.MODEL_PATH]
    sources = params[RequestParams.SOURCES]
    targets = params[RequestParams.TARGETS]
    base_model = params[RequestParams.BASE_MODEL]
    ModelFineTuneArgs(model_path=model_path, s_arts=sources, t_arts=targets, )
