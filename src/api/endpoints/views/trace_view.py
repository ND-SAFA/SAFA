import os.path
from typing import Type, Union

from api.endpoints.common.endpoint_decorator import endpoint
from api.endpoints.views.predict_serializer import PredictionSerializer, TraceRequest
from api.utils.view_util import ViewUtil
from tgen.common.constants.dataset_constants import NO_CHECK
from tgen.common.constants.ranking_constants import DEFAULT_SEARCH_EMBEDDING_MODEL, DEFAULT_SEARCH_FILTER
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.jobs.tracing_jobs.tracing_job import TracingJob
from tgen.tracing.ranking.supported_ranking_pipelines import SupportedRankingPipelines

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


def perform_tracing_job(dataset: ApiDefinition, job: Union[Type[RankingJob], Type[TracingJob]], **kwargs):
    eval_project_reader = ApiProjectReader(api_definition=dataset)
    eval_dataset_creator = TraceDatasetCreator(project_reader=eval_project_reader, allowed_orphans=NO_CHECK)
    prompt_dataset_creator = PromptDatasetCreator(trace_dataset_creator=eval_dataset_creator, project_summary=dataset.summary)
    tracing_job = job(dataset_creator=prompt_dataset_creator, **kwargs)
    prediction_result = ViewUtil.run_job(tracing_job)

    return {"predictions": prediction_result.prediction_entries}


@endpoint(PredictionSerializer, is_async=True)
def perform_prediction(prediction_payload: TraceRequest):
    dataset: ApiDefinition = prediction_payload["dataset"]
    return perform_tracing_job(dataset,
                               RankingJob,
                               select_top_predictions=False)


@endpoint(PredictionSerializer)
def perform_search(prediction_payload: TraceRequest):
    dataset: ApiDefinition = prediction_payload["dataset"]
    return perform_tracing_job(dataset,
                               RankingJob,
                               ranking_pipeline=SupportedRankingPipelines.SEARCH,
                               max_children_per_query=DEFAULT_SEARCH_FILTER,
                               embedding_model_name=DEFAULT_SEARCH_EMBEDDING_MODEL,
                               select_top_predictions=False,
                               sorter="embedding")
