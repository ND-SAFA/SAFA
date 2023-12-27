from api.endpoints.common.dataset_converter import create_api_dataset
from api.endpoints.common.endpoint_decorator import endpoint
from api.endpoints.serializers.summarize_serializer import SummarizeRequest, SummarizeSerializer
from api.utils.view_util import ViewUtil
from tgen.jobs.summary_jobs.summarize_job import SummarizeJob


@endpoint(SummarizeSerializer)
def perform_summarization_sync(request_data: SummarizeRequest):
    return perform_summarize_request(request_data)


@endpoint(SummarizeSerializer, is_async=True)
def perform_summarization_job(request_data: SummarizeRequest):
    return perform_summarize_request(request_data)


LAYER_ID = "SUMMARIZE_LAYER_ID"


def perform_summarize_request(data: SummarizeRequest):
    """
    Performs artifact summarization.
    :param data: Serialized data.
    :return: The same artifacts with content as summary.
    """
    dataset_creator = create_api_dataset(data.artifacts, project_summary=data.project_summary)
    summarize_job = SummarizeJob(dataset_creator=dataset_creator)
    summarized_artifacts = ViewUtil.run_job(summarize_job)
    return summarized_artifacts
