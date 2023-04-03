import json
import os.path
from typing import Any, Dict, Union

from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.openapi import Schema, TYPE_OBJECT
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from cloud.model_utility import CloudUtility
from experiment_creator import ExperimentCreator, PredictionJobTypes
from serializers.prediction_serializer import PredictionSerializer
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.experiments.experiment import Experiment
from tgen.jobs.components.job_result import JobResult
from tgen.util.definition_creator import DefinitionCreator


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
        temp_dir = os.path.expanduser("~/desktop/safa/openai/output")

        prediction_job_args = {
            "dataset": dataset,
            "output_dir": temp_dir
        }
        if model != "gpt":
            prediction_job_args["prediction_job_type"] = PredictionJobTypes.OPENAI
        else:
            model_path = CloudUtility.download_model(model)
            prediction_job_args["prediction_job_type"] = PredictionJobTypes.BASE
            prediction_job_args["model_path"] = model_path

        # Assign output path based on random ID
        experiment_definition = ExperimentCreator.create_prediction_definition(**prediction_job_args)
        experiment: Experiment = DefinitionCreator.create(Experiment, experiment_definition)
        experiment.run()
        return experiment.steps[0].jobs[0].result

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
