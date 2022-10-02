import json
from abc import ABC
from typing import Dict, Union

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from common.api.responses import BaseResponse
from common.api.request_serializers import PredictSerializer, TrainSerializer, BaseTraceSerializer
from common.storage.safa_storage import SafaStorage
from server.job_type import JobType
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from drf_yasg.openapi import Schema, TYPE_OBJECT

SERIALIZERS = {JobType.MODEL: BaseTraceSerializer,
               JobType.PREDICT: PredictSerializer,
               JobType.TRAIN: TrainSerializer}


class BaseTraceJobView(APIView, ABC):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get_responses(response_keys: Union[str, list]) -> Dict:
        """
        Gets properties used to generate response documentation
        :param response_keys: either a single response key or a list of response keys to get properties for
        :return: the response dictionary
        """
        return {
            status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                                       properties=BaseResponse.get_properties(response_keys))}

    @staticmethod
    def _request_to_dict(request: HttpRequest) -> Dict:
        """
        Converts a HttpRequest to a dictionary
        :param request: the HttpRequest
        :return: a dictionary containing the information from the request body
        """
        return json.loads(request.body)

    @staticmethod
    def _run_job(request: HttpRequest, job_type: JobType, run_async: bool = True) -> JsonResponse:
        """
        Runs the specified job using params from a given request
        :param request: request from client
        :param job_type: job type to run
        :param run_async:
        :return: the job name
        """
        data = BaseTraceJobView._request_to_dict(request)
        serializer = SERIALIZERS[job_type](data=data)
        if serializer.is_valid():
            args_builder = serializer.save()
            job = job_type.value(args_builder)
            job.start()
            if run_async:
                response_dict = {BaseResponse.JOB_ID: str(job.id)}
            else:
                job.join()
                response_dict = job.result
            SafaStorage.remove_mount_directory(job.output_filepath)
            return JsonResponse(response_dict)
        return JsonResponse(serializer.errors)


class ModelView(BaseTraceJobView):
    job_type = JobType.MODEL
    responses = BaseTraceJobView.get_responses([BaseResponse.MODEL_PATH, BaseResponse.STATUS, BaseResponse.EXCEPTION])

    @csrf_exempt
    @swagger_auto_schema(request_body=SERIALIZERS[job_type], responses=responses)
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        For creating a new model
        :param: the http request
        :return JSONResponse including the model path or exception and status of the job
        """
        return self._run_job(request, self.job_type, run_async=False)


class PredictView(BaseTraceJobView):
    job_type = JobType.PREDICT
    responses = BaseTraceJobView.get_responses([BaseResponse.JOB_ID])

    @csrf_exempt
    @swagger_auto_schema(request_body=SERIALIZERS[job_type], responses=responses)
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        For generating trace links from artifacts
        :param: the http request
        :return JSONResponse including the job id
        """
        return self._run_job(request, self.job_type)


class TrainView(BaseTraceJobView):
    job_type = JobType.TRAIN
    responses = BaseTraceJobView.get_responses([BaseResponse.JOB_ID])

    @csrf_exempt
    @swagger_auto_schema(request_body=SERIALIZERS[job_type], responses=responses)
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        For training a model on project data
        :param: the http request
        :return JSONResponse including the job id
        """
        return self._run_job(request, self.job_type)
