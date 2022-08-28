import json
from copy import deepcopy
from typing import Dict

import numpy as np
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from server.api import Api
from server.job_type import JobType
from trace.config.constants import VALIDATION_PERCENTAGE_DEFAULT
from trace.jobs.trace_args_builder import TraceArgsBuilder
from server.job_type import JobType
import json


@csrf_exempt
def predict(request: HttpRequest) -> JsonResponse:
    """
    For generating trace links from artifacts
    :param request: request from client containing model and artifact information
    :return: output of prediction
    """
    return _run_job(request, JobType.PREDICT)


def fine_tune(request: HttpRequest) -> JsonResponse:
    """
    For fine-tuning a model on project data
    :param request: request from client containing model and artifact information
    :return: output of training
    """
    return _run_job(request, JobType.TRAIN)


def _run_job(request: HttpRequest, job_type: JobType) -> JsonResponse:
    """
    Runs the specified job using params from a given request
    :param request: request from client
    :param job_type: job type to run
    :return: the job name
    """
    request_dict = _request_to_dict(request)
    args = _make_job_params_from_request(request_dict)
    job = job_type.value(args)
    job.start()
    return JsonResponse({Api.JOB_ID.value: job.id})


def _make_job_params_from_request(request_dict: Dict) -> TraceArgsBuilder:
    """
    Extracts necessary information from a request and creates an arg builder from it
    :param request_dict: a dictionary from the request body
    :return: a TraceArgsBuilder for the request
    """
    params = deepcopy(request_dict)
    model_path = params.pop(Api.MODEL_PATH.value)
    sources = params.pop(Api.SOURCES.value)
    targets = params.pop(Api.TARGETS.value)
    base_model = params.pop(Api.BASE_MODEL.value)
    output_path = params.pop(Api.OUTPUT_PATH.value)
    links = _safe_pop(params, Api.LINKS.value)  # optional
    return TraceArgsBuilder(base_model, model_path, output_path, sources, targets, links, VALIDATION_PERCENTAGE_DEFAULT, **params)


def _safe_pop(dict_: Dict, key: any, default: any = None) -> any:
    """
    Safely removes a value from dictionary, returning a default value if the key is not in the dictionary
    :param dict_: the dictionary
    :param key: the key to pop
    :param default: default value to return if key is not in the dictionary
    :return: dictionary element that was popped or default
    """
    return dict_.pop(key) if key in dict_ else default


def _request_to_dict(request: HttpRequest) -> Dict:
    """
    Converts a HttpRequest to a dictionary
    :param request: the HttpRequest
    :return: a dictionary containing the information from the request body
    """
    return json.loads(request.body)
