import json
from typing import Any, Dict, Union

from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.openapi import Schema, TYPE_OBJECT
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from data.readers.definitions.api_definition import ApiDefinition
from serializers.prediction_serializer import PredictionSerializer
from tgen.src.jobs.components.job_result import JobResult


def get_responses(response_keys: Union[str, list]) -> Dict:
    """
    Gets properties used to generate response documentation
    :param response_keys: either a single response key or a list of response keys to get properties for
    :return: the response dictionary
    """
    return {
        status.HTTP_200_OK: Schema(type=TYPE_OBJECT,
                                   properties=JobResult.get_properties(response_keys))}


class PredictView(APIView):
    """
    Allows users to run experiments.
    """

    @csrf_exempt
    @swagger_auto_schema(request_body=PredictionSerializer,
                         responses=get_responses([JobResult.MODEL_PATH, JobResult.STATUS, JobResult.EXCEPTION]))
    def post(self, request: HttpRequest):
        prediction_payload = self.read_request(request, PredictionSerializer)
        model = prediction_payload["model"]
        dataset: ApiDefinition = prediction_payload["dataset"]
        # TODO: Create definition JSON for experiment and run.
        raise NotImplementedError("Current building out prediction endpoint.")

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
        if serializer.is_valid():
            return serializer.save()
        raise Exception(serializer.errors)
