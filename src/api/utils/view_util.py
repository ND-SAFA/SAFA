import json
from typing import Any, Type
from uuid import UUID

from django.http import HttpRequest
from rest_framework import serializers

from tgen.jobs.abstract_job import AbstractJob
from tgen.util.status import Status


class ViewUtil:
    """
    Contains utility methods for handling requests threw views.
    """

    @staticmethod
    def run_job(abstract_job: AbstractJob):
        """
        Runs job and performs error handling.
        :param abstract_job: The job to run.
        :return: The result of the job.
        """
        job_result = abstract_job.run()
        job_status = job_result.status
        job_result = job_result.to_json(as_dict=True)
        if job_status == Status.FAILURE:
            raise Exception(job_result["body"])
        job_body = job_result["body"]
        return job_body

    @staticmethod
    def read_request(request: HttpRequest, serializer_class: Type[serializers.Serializer]) -> Any:
        """
        Converts a HttpRequest to a dictionary
        :param request: the HttpRequest
        :param serializer_class: The class used to serialize request body
        :return: a dictionary containing the information from the request body
        """
        data = json.loads(request.body)
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return obj

    @staticmethod
    def is_uuid(model_id: str, version=4) -> bool:
        """
        Returns whether given id is a uuid
        :param model_id: The model id to check.
        :param version: The UUID version.
        :return: True if uuid is given.
        """
        try:
            uuid_obj = UUID(model_id, version=version)
        except ValueError:
            return False
        return str(uuid_obj) == model_id
