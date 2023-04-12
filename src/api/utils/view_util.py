import json
from typing import Any, Dict, Union
from uuid import UUID

from django.http import HttpRequest
from drf_yasg.openapi import Schema, TYPE_OBJECT
from rest_framework import status

from tgen.jobs.components.job_result import JobResult


class ViewUtil:
    """
    Contains utility methods for handling requests threw views.
    """

    @staticmethod
    def read_request(request: HttpRequest, serializer_class) -> Any:
        """
        Converts a HttpRequest to a dictionary
        :param request: the HttpRequest
        :param serializer_class: The class used to serialize request body
        :return: a dictionary containing the information from the request body
        """
        data = json.loads(request.body)
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

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
