import os.path
import os.path
import uuid
from typing import Dict

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api.experiment_creator import JobCreator, PredictionJobTypes, PredictionJobs
from api.serializers.prediction_serializer import PredictionSerializer
from api.utils.view_util import ViewUtil
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.components.job_result import JobResult
from tgen.testres.definition_creator import DefinitionCreator
from tgen.util.json_util import NpEncoder

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


def create_predict_definition(task_id: str, dataset: ApiDefinition, model: str) -> PredictionJobs:
    """
    Creates definition for a prediction job on given dataset using defined model.
    :param task_id: The UUID of the task.
    :param dataset: The dataset to predict on.
    :param model: The model used to make predictions.
    :return: The JSON job definition.
    """
    prediction_job_args = {
        "output_dir": os.path.join(JOB_DIR, task_id),
        "prediction_job_type": PredictionJobTypes.OPENAI if model == "gpt" else PredictionJobTypes.BASE,
        "model_path": model}

    return JobCreator.create_prediction_definition(dataset=dataset, **prediction_job_args)


class PredictView(APIView):
    """
    Allows users to run experiments.
    """

    @csrf_exempt
    @swagger_auto_schema(request_body=PredictionSerializer,
                         responses=ViewUtil.get_responses([JobResult.MODEL_PATH, JobResult.STATUS, JobResult.EXCEPTION]))
    def post(self, request: HttpRequest):
        prediction_payload = ViewUtil.read_request(request, PredictionSerializer)
        model = prediction_payload["model"]
        dataset_definition: Dict = prediction_payload["dataset"]
        dataset: ApiDefinition = DefinitionCreator.create(ApiDefinition, dataset_definition)

        api_id = uuid.uuid4()
        prediction_job = create_predict_definition(str(api_id), dataset, model)
        prediction_job.run()
        output = prediction_job.result.to_json(as_dict=True)
        return JsonResponse({"predictions": output["prediction_entries"]}, encoder=NpEncoder)
