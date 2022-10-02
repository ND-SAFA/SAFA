import json
from typing import Dict

from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from common.api.responses import BaseResponse
from common.api.request_serializers import PredictSerializer, TrainSerializer, BaseTraceSerializer
from common.storage.safa_storage import SafaStorage
from server.job_type import JobType

SERIALIZERS = {JobType.MODEL: BaseTraceSerializer,
               JobType.PREDICT: PredictSerializer,
               JobType.TRAIN: TrainSerializer}


@csrf_exempt
def create_model(request: HttpRequest) -> HttpResponse:
    """
    For creating a new model
    :param request: request from client containing model information
    :return: new model file path
    """
    return _run_job(request, JobType.MODEL, run_async=False)


@csrf_exempt
def predict(request: HttpRequest) -> JsonResponse:
    """
    For generating trace links from artifacts
    :param request: request from client containing model and artifact information
    :return: job id
    """
    return _run_job(request, JobType.PREDICT)


@csrf_exempt
def train(request: HttpRequest) -> JsonResponse:
    """
    For fine-tuning a model on project data
    :param request: request from client containing model and artifact information
    :return: job id
    """
    return _run_job(request, JobType.TRAIN)


def _request_to_dict(request: HttpRequest) -> Dict:
    """
    Converts a HttpRequest to a dictionary
    :param request: the HttpRequest
    :return: a dictionary containing the information from the request body
    """
    return json.loads(request.body)


def _run_job(request: HttpRequest, job_type: JobType, run_async: bool = True) -> JsonResponse:
    """
    Runs the specified job using params from a given request
    :param request: request from client
    :param job_type: job type to run
    :param run_async:
    :return: the job name
    """
    data = _request_to_dict(request)
    serializer = SERIALIZERS[job_type](data=data)
    if serializer.is_valid():
        args_builder = serializer.save()
        job = job_type.value(args_builder)
        job.start()
        if run_async:
            response_dict = {BaseResponse.JOB_ID: job.id}
        else:
            job.join()
            response_dict = job.result
        SafaStorage.remove_mount_directory(job.output_filepath)
        return JsonResponse(response_dict)
    return JsonResponse(serializer.errors)
