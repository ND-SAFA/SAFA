import os.path
import uuid
from typing import Type, Union

from api.endpoints.base.views.endpoint import async_endpoint, endpoint
from api.endpoints.predict.predict_serializer import PredictionPayload, PredictionSerializer
from api.utils.view_util import ViewUtil
from tgen.constants.dataset_constants import NO_CHECK_VALUE
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.trainer_jobs.ranking_job import RankingJob
from tgen.jobs.trainer_jobs.tracing_job import TracingJob
from tgen.testres.definition_creator import DefinitionCreator
from tgen.util.logging.logger_manager import logger

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


def perform_tracing_job(dataset_definition: ApiDefinition, job: Union[Type[RankingJob], Type[TracingJob]]):
    print("TRACING (with print)")
    logger.info("TRACING (with logger)")
    dataset: ApiDefinition = DefinitionCreator.create(ApiDefinition, dataset_definition)

    api_id = uuid.uuid4()
    eval_project_reader = ApiProjectReader(api_definition=dataset)
    eval_dataset_creator = TraceDatasetCreator(project_reader=eval_project_reader, allowed_orphans=NO_CHECK_VALUE)
    trainer_dataset_manager = TrainerDatasetManager(eval_dataset_creator=eval_dataset_creator)
    tracing_job = job(trainer_dataset_manager=trainer_dataset_manager)
    prediction_result = ViewUtil.run_job(tracing_job)

    return {"predictions": prediction_result.prediction_entries}


@async_endpoint(PredictionSerializer)
def perform_prediction(prediction_payload: PredictionPayload):
    return perform_tracing_job(prediction_payload["dataset"], RankingJob)


@endpoint(PredictionSerializer)
def perform_search(prediction_payload: PredictionPayload):
    return perform_tracing_job(prediction_payload["dataset"], RankingJob)
