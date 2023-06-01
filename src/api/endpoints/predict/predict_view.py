import os.path
import os.path
import uuid
from typing import Optional

from api.endpoints.base.views.endpoint import async_endpoint, endpoint
from api.endpoints.predict.predict_serializer import PredictionPayload, PredictionSerializer
from api.experiment_creator import JobCreator, PredictionJobTypes
from api.utils.model_util import ModelUtil
from api.utils.view_util import ViewUtil
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob
from tgen.testres.definition_creator import DefinitionCreator
from tgen.util.logging.logger_manager import logger

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


def p(prediction_payload: PredictionPayload):
    model = prediction_payload.get("model", "gpt")
    dataset_definition: ApiDefinition = prediction_payload["dataset"]
    prompt: Optional[str] = prediction_payload.get("prompt", None)
    dataset: ApiDefinition = DefinitionCreator.create(ApiDefinition, dataset_definition)

    api_id = uuid.uuid4()
    prediction_job = create_predict_definition(str(api_id), dataset, model, prompt)

    prediction_result = ViewUtil.run_job(prediction_job)

    return {"predictions": prediction_result.prediction_entries}


@async_endpoint(PredictionSerializer)
def perform_prediction(prediction_payload: PredictionPayload):
    return p(prediction_payload)


@endpoint(PredictionSerializer)
def perform_prediction_sync(payload: PredictionPayload):
    return p(payload)
