import os.path
from typing import Type, Union

from api.endpoints.base.views.endpoint import async_endpoint, endpoint
from api.endpoints.predict.predict_serializer import PredictionPayload, PredictionSerializer
from api.utils.view_util import ViewUtil
from tgen.constants.dataset_constants import NO_CHECK_VALUE
from tgen.constants.tgen_constants import DEFAULT_SEARCH_MODEL, SEARCH_CHILD_TYPE, SEARCH_PARENT_TYPE
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.trainer_jobs.ranking_job import RankingJob
from tgen.jobs.trainer_jobs.tracing_job import TracingJob

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


def perform_tracing_job(dataset: ApiDefinition, job: Union[Type[RankingJob], Type[TracingJob]], **kwargs):
    eval_project_reader = ApiProjectReader(api_definition=dataset)
    eval_dataset_creator = TraceDatasetCreator(project_reader=eval_project_reader, allowed_orphans=NO_CHECK_VALUE)
    tracing_job = job(dataset_creator=eval_dataset_creator, **kwargs)
    prediction_result = ViewUtil.run_job(tracing_job)

    return {"predictions": prediction_result.prediction_entries}


@async_endpoint(PredictionSerializer)
def perform_prediction(prediction_payload: PredictionPayload):
    return perform_tracing_job(prediction_payload["dataset"], RankingJob, select_top_predictions=False)


@endpoint(PredictionSerializer)
def perform_search(prediction_payload: PredictionPayload):
    dataset = prediction_payload["dataset"]
    summary = prediction_payload.get("summary", None)
    return perform_tracing_job(dataset,
                               RankingJob,
                               generate_summary=False,
                               project_summary=summary,
                               max_children_per_query=50,
                               model=DEFAULT_SEARCH_MODEL,
                               layer_ids=[SEARCH_PARENT_TYPE, SEARCH_CHILD_TYPE])
