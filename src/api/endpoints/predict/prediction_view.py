import os.path
import os.path
import uuid
from typing import Dict, Optional

from rest_framework.views import APIView

from api.endpoints.base.views.endpoint import endpoint
from api.endpoints.predict.prediction_serializer import PredictionSerializer
from api.experiment_creator import JobCreator, PredictionJobTypes
from api.utils.model_util import ModelUtil
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob
from tgen.testres.definition_creator import DefinitionCreator
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


def create_predict_definition(task_id: str, dataset: ApiDefinition, model: str, prompt: str) -> AbstractTrainerJob:
    """
    Creates definition for a prediction job on given dataset using defined model.
    :param task_id: The UUID of the task.
    :param dataset: The dataset to predict on.
    :param model: The model used to make predictions.
    :return: The JSON job definition.
    """
    prediction_job_args = {
        "output_dir": os.path.join(JOB_DIR, task_id),
        "prediction_job_type": PredictionJobTypes.LLM if ModelUtil.is_llm(model) else PredictionJobTypes.BASE,
        "model_path": model
    }
    if prompt:
        prediction_job_args["prompt_creator"] = ClassificationPromptCreator(base_prompt=prompt)
    return JobCreator.create_prediction_definition(dataset=dataset, **prediction_job_args)


class PredictView(APIView):
    """
    Allows users to run experiments.
    """

    @endpoint(serializer=PredictionSerializer)
    def post(self, prediction_payload):
        model = prediction_payload["model"]
        dataset_definition: Dict = prediction_payload["dataset"]
        prompt: Optional[str] = prediction_payload.get("prompt", None)

        dataset: ApiDefinition = DefinitionCreator.create(ApiDefinition, dataset_definition)

        api_id = uuid.uuid4()
        prediction_job = create_predict_definition(str(api_id), dataset, model, prompt)

        def post_process(trace_output: TracePredictionOutput):
            return {"predictions": trace_output.prediction_entries}

        return prediction_job, post_process
