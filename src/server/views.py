import json
from abc import ABC
from typing import Dict, Union

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from drf_yasg.openapi import Schema, TYPE_OBJECT
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView

from common.api.request_serializers import BaseTraceSerializer, PredictSerializer, TrainSerializer
from common.api.responses import BaseResponse
from common.jobs.abstract_job import AbstractJob
from server.job_type import JobType

SERIALIZERS = {JobType.CREATE_MODEL: BaseTraceSerializer,
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
    def request_to_dict(request: HttpRequest) -> Dict:
        """
        Converts a HttpRequest to a dictionary
        :param request: the HttpRequest
        :return: a dictionary containing the information from the request body
        """
        return json.loads(request.body)

    @staticmethod
    def dict_to_response(dict_: Dict) -> JsonResponse:
        """
        Converts a dictionary to a JsonResponse
        :param dict_: a dictionary
        :return: the json response
        """
        return JsonResponse(dict_)

    @staticmethod
    def run_job(request: HttpRequest, job_type: JobType, job: AbstractJob = None,
                run_async: bool = True) -> JsonResponse:
        """
        Runs the specified job using params from a given request
        :param request: request from client
        :param job_type: job type to run
        :param run_async: if True, runs the job asynchronously
        :param job: the job to run (if none is provided, one will be created from the request)
        :return: the job name
        """
        if not job:
            job = BaseTraceJobView._create_job_from_request(request, job_type)
        if isinstance(job, AbstractJob):
            job.start()
            if run_async:
                response_dict = {BaseResponse.JOB_ID: str(job.id)}
            else:
                job.join()
                response_dict = job.result
        else:
            response_dict = job
        return BaseTraceJobView.dict_to_response(response_dict)

    @staticmethod
    def _create_job_from_request(request: HttpRequest, job_type: JobType) -> Union[AbstractJob, dict]:
        """
        Serializes the request data
        :param request: the HTTP request
        :param job_type: the job type
        :return either the job or a dictionary containing the serializer errors
        """
        data = BaseTraceJobView.request_to_dict(request)
        serializer = SERIALIZERS[job_type](data=data)
        if serializer.is_valid():
            args_builder = serializer.save()
            job = job_type.value(args_builder)
            return job
        return serializer.errors


class CreateModelView(BaseTraceJobView):
    job_type = JobType.CREATE_MODEL
    responses = BaseTraceJobView.get_responses([BaseResponse.MODEL_PATH, BaseResponse.STATUS, BaseResponse.EXCEPTION])

    @swagger_auto_schema(request_body=SERIALIZERS[job_type], responses=responses)
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        For creating a new model
        :param: the http request
        :return JSONResponse including the model path or exception and status of the job
        """
        return self.run_job(request, self.job_type, run_async=False)


class PredictView(BaseTraceJobView):
    job_type = JobType.PREDICT
    responses = BaseTraceJobView.get_responses([BaseResponse.JOB_ID])

    @swagger_auto_schema(request_body=SERIALIZERS[job_type], responses=responses)
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        For generating trace links from artifacts
        :param: the http request
        :return JSONResponse including the job id
        """
        return self.run_job(request, self.job_type)


class TrainView(BaseTraceJobView):
    job_type = JobType.TRAIN
    responses = BaseTraceJobView.get_responses([BaseResponse.JOB_ID])

    @swagger_auto_schema(request_body=SERIALIZERS[job_type], responses=responses)
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        For training a model on project data
        :param: the http request
        :return JSONResponse including the job id
        """
        return self.run_job(request, self.job_type)


class DeleteModelView(BaseTraceJobView):
    job_type = JobType.DELETE_MODEL
    request = Schema(type=TYPE_OBJECT, properties=BaseResponse.get_properties([BaseResponse.MODEL_PATH]))
    responses = BaseTraceJobView.get_responses([BaseResponse.STATUS, BaseResponse.EXCEPTION])

    @swagger_auto_schema(request_body=request, responses=responses)
    def post(self, request: HttpRequest) -> JsonResponse:
        """
        For deleting a model directory
        :param: the http request
        :return JSONResponse including the status of the job and the exception if one occurred
        """
        output_dir = self.request_to_dict(request).get(BaseResponse.MODEL_PATH, None)
        if not output_dir:
            response_dict = {BaseResponse.MODEL_PATH: "This is required."}
        else:
            job = self.job_type.value(output_dir)
            self.run_job(request, self.job_type, job, run_async=False)
            response_dict = job.result
        return BaseTraceJobView.dict_to_response(response_dict)
