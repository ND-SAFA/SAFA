import json
from typing import Dict, Type, TypeVar, Union

from django.http.request import HttpRequest
from drf_yasg.openapi import Schema, TYPE_OBJECT
from rest_framework import permissions, status
from rest_framework.views import APIView

from api.responses.base_response import BaseResponse
from server.serializers.base_serializer import BaseSerializer

AppEntity = TypeVar("AppEntity")


class AbstractTraceView(APIView):
    permission_classes = (permissions.AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
    def read_request(request: HttpRequest, serializer_class: Type[BaseSerializer[AppEntity]]) -> AppEntity:
        """
        Converts a HttpRequest to a dictionary
        :param request: the HttpRequest
        :param serializer_class: The class used to serialize request body
        :return: a dictionary containing the information from the request body
        """
        data = json.loads(request.body)
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            return serializer.save()
        raise Exception(serializer.errors)
