import os.path
from typing import List, Type, TypedDict, Union

from api.endpoints.gen.trace.trace_serializer import TraceRequest, TraceSerializer
from api.endpoints.handler.endpoint_decorator import endpoint
from api.utils.view_util import ViewUtil
from tgen.common.constants.dataset_constants import NO_CHECK
from tgen.common.constants.ranking_constants import DEFAULT_SEARCH_EMBEDDING_MODEL, DEFAULT_SEARCH_FILTER
from tgen.common.objects.trace import Trace
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.jobs.tracing_jobs.tracing_job import TracingJob
from tgen.tracing.ranking.sorters.supported_sorters import SupportedSorter
from tgen.tracing.ranking.supported_ranking_pipelines import SupportedRankingPipelines

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


class TracingOutput(TypedDict):
    """
    The output from a tracing job.
    """
    predictions: List[Trace]


def perform_tracing_job(dataset: ApiDefinition, job: Union[Type[RankingJob], Type[TracingJob]], **kwargs) -> TracingOutput:
    """
    Runs a tracing job on given dataset.
    :param dataset: The dataset containing artifacts to compare.
    :param job: The job type to creat and run.
    :param kwargs: Additional keyword arguments to construct job.
    :return: The tracing output.
    """
    job_args = ViewUtil.create_job_args_from_api_definition(dataset)
    tracing_job = job(job_args, **kwargs)
    prediction_result = ViewUtil.run_job(tracing_job)

    return {"predictions": prediction_result.prediction_entries}


@endpoint(TraceSerializer, is_async=True)
def perform_trace_prediction(prediction_payload: TraceRequest) -> TracingOutput:
    """
    Performs embedding search and LLM review on rankings to create trace links.
    :param prediction_payload: Dataset containing sources and targets to compare.
    :return: List of trace links generated.
    """
    dataset: ApiDefinition = prediction_payload["dataset"]
    return perform_tracing_job(dataset,
                               RankingJob,
                               select_top_predictions=False)


@endpoint(TraceSerializer)
def perform_embedding_search(prediction_payload: TraceRequest) -> TracingOutput:
    """
    Searches dataset against targets using the similarity scores from their embeddings.
    :param prediction_payload: Dataset containing source and targets to compare.
    :return: List of trace links.
    """
    dataset: ApiDefinition = prediction_payload["dataset"]
    return perform_tracing_job(dataset,
                               RankingJob,
                               ranking_pipeline=SupportedRankingPipelines.SEARCH,
                               max_children_per_query=DEFAULT_SEARCH_FILTER,
                               embedding_model_name=DEFAULT_SEARCH_EMBEDDING_MODEL,
                               select_top_predictions=False,
                               sorter=SupportedSorter.TRANSFORMER)
