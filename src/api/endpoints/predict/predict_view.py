import os.path
import os.path
import uuid

from celery import shared_task

from api.endpoints.base.views.endpoint import endpoint
from api.endpoints.predict.predict_serializer import PredictionPayload, PredictionSerializer
from api.experiment_creator import JobCreator, PredictionJobTypes
from api.utils.view_util import ViewUtil
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob
from tgen.testres.definition_creator import DefinitionCreator
from tgen.util.logging.logger_manager import logger

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


def create_predict_definition(task_id: str, dataset: ApiDefinition) -> AbstractTrainerJob:
    """
    Creates definition for a prediction job on given dataset using defined model.
    :param task_id: The UUID of the task.
    :param dataset: The dataset to predict on.
    :return: The JSON job definition.
    """
    output_dir = os.path.join(JOB_DIR, task_id)
    return JobCreator.create_prediction_definition(dataset=dataset, output_dir=output_dir,
                                                   prediction_job_type=PredictionJobTypes.LLM)


def create_payload_log(prediction_payload: PredictionPayload) -> str:
    return f"Prediction Payload\nModel: {prediction_payload['model']}\n"


@endpoint(PredictionSerializer)
@shared_task
def predict(prediction_payload: PredictionPayload):
    logger.info(create_payload_log(prediction_payload))
    dataset_definition: ApiDefinition = prediction_payload["dataset"]

    dataset: ApiDefinition = DefinitionCreator.create(ApiDefinition, dataset_definition)

    api_id = uuid.uuid4()
    prediction_job = create_predict_definition(str(api_id), dataset)

    prediction_result = ViewUtil.run_job(prediction_job)
    return {"predictions": prediction_result.prediction_entries}
