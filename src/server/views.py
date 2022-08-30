import json
import os
import uuid
from copy import deepcopy
from typing import Dict

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from common.api.prediction_request import PredictionRequest
from server.job_type import JobType
from trace.config.constants import VALIDATION_PERCENTAGE_DEFAULT
from trace.jobs.trace_args_builder import TraceArgsBuilder


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
    output_path = args.output_path
    return JsonResponse({"outputPath": output_path})


def _make_job_params_from_request(request_dict: Dict) -> TraceArgsBuilder:
    """
    Extracts necessary information from a request and creates an arg builder from it
    :param request_dict: a dictionary from the request body
    :return: a TraceArgsBuilder for the request
    """
    params = deepcopy(request_dict)
    model_path = params.pop(PredictionRequest.MODEL_PATH)
    sources = params.pop(PredictionRequest.SOURCES)
    targets = params.pop(PredictionRequest.TARGETS)
    base_model = params.pop(PredictionRequest.BASE_MODEL)
    output_path = params.pop(PredictionRequest.OUTPUT_PATH)
    links = _safe_pop(params, PredictionRequest.LINKS)  # optional
    return TraceArgsBuilder(base_model, model_path, output_path, sources, targets, links, VALIDATION_PERCENTAGE_DEFAULT,
                            **params)


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
