import json
from typing import Dict, Type, TypeVar, Union

from django.http import JsonResponse
from django.http.request import HttpRequest
from drf_yasg.openapi import Schema, TYPE_OBJECT
from rest_framework import permissions, status
from rest_framework.views import APIView

from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult
from jobs.job_factory import JobFactory

AppEntity = TypeVar("AppEntity")


class AbstractTraceView(APIView):
    permission_classes = (permissions.AllowAny,)

    def __init__(self, serializer, job: Type[AbstractJob], **kwargs, ):
        """
        :param serializer_class: The serializer used to validate request and create job.
        :param job_class: The class of the job to run.
        :param kwargs: Custom view arguments
        """
        super().__init__(**kwargs)
        self.serializer = serializer
        self.job = job

    def run_job(self, request: HttpRequest, job: AbstractJob = None, run_async: bool = True) -> JsonResponse:
        """
        Serializes request, create job, and runs it.
        :param request: request from client.

        :param run_async: If True, runs the job asynchronously
        :param job: the job to run (if none is provided, one will be created from the request)
        :return: the job name
        """
        if not job:
            job_factory = AbstractTraceView.read_request(request, self.serializer)
            job = job_factory.build(self.job)
        job.run()
        if run_async:
            response_dict = {JobResult.JOB_ID: str(job.id)}
        else:
            job.join()
            response_dict = job.result.as_dict()
        return AbstractTraceView.dict_to_response(response_dict)

    @staticmethod
    def dict_to_response(dict_: Dict) -> JsonResponse:
        """
        Converts a dictionary to a JsonResponse
        :param dict_: a dictionary
        :return: the json response
        """
        return JsonResponse(dict_)

    @staticmethod
    def get_responses(response_keys: Union[str, list]) -> Dict:
        """
        Gets properties used to generate response documentation
        :param response_keys: either a single response key or a list of response keys to get properties for
        :return: the response dictionary
        """
        return {
            status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                                       properties=JobResult.get_properties(response_keys))}

    @staticmethod
    def read_request(request: HttpRequest, serializer_class) -> JobFactory:
        """
        Converts a HttpRequest to a dictionary
        :param request: the HttpRequest
        :param serializer_class: The class used to serialize request body
        :return: a dictionary containing the information from the request body
        """
        data = json.loads(request.body)
        serializer = serializer_class(data=data)
        if serializer.is_format():
            return serializer.save()
        raise Exception(serializer.errors)
