import json
import os.path
from typing import Type, Union

from api.endpoints.base.views.endpoint import async_endpoint, endpoint
from api.endpoints.predict.predict_serializer import PredictionSerializer, TraceRequest
from api.utils.view_util import ViewUtil
from tgen.common.util.json_util import NpEncoder
from tgen.common.util.logging.logger_manager import logger
from tgen.constants.dataset_constants import NO_CHECK
from tgen.constants.tgen_constants import DEFAULT_SEARCH_FILTER, DEFAULT_SEARCH_MODEL, SEARCH_CHILD_TYPE, SEARCH_PARENT_TYPE
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.jobs.tracing_jobs.tracing_job import TracingJob

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


def perform_tracing_job(dataset: ApiDefinition, job: Union[Type[RankingJob], Type[TracingJob]], **kwargs):
    eval_project_reader = ApiProjectReader(api_definition=dataset)
    eval_dataset_creator = TraceDatasetCreator(project_reader=eval_project_reader, allowed_orphans=NO_CHECK)
    tracing_job = job(dataset_creator=eval_dataset_creator, **kwargs)
    prediction_result = ViewUtil.run_job(tracing_job)

    result = json.dumps(prediction_result, cls=NpEncoder)
    logger.info("\n\n" + result)

    return {"predictions": prediction_result.prediction_entries}


@async_endpoint(PredictionSerializer)
def perform_prediction(prediction_payload: TraceRequest):
    dataset: ApiDefinition = prediction_payload["dataset"]
    summary = dataset.summary
    return perform_tracing_job(dataset,
                               RankingJob,
                               select_top_predictions=False,
                               project_summary=summary)


@endpoint(PredictionSerializer)
def perform_search(prediction_payload: TraceRequest):
    dataset: ApiDefinition = prediction_payload["dataset"]
    summary = dataset.summary
    return perform_tracing_job(dataset,
                               RankingJob,
                               generate_summary=False,
                               project_summary=summary,
                               max_children_per_query=DEFAULT_SEARCH_FILTER,
                               model=DEFAULT_SEARCH_MODEL,
                               layer_ids=[SEARCH_PARENT_TYPE, SEARCH_CHILD_TYPE])
