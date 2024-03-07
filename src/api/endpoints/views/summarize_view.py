from api.endpoints.common.dataset_converter import create_api_dataset
from api.endpoints.common.endpoint_decorator import endpoint
from api.endpoints.serializers.summarize_serializer import SummarizeRequest, SummarizeSerializer
from api.utils.view_util import ViewUtil
from tgen.jobs.summary_jobs.summarize_job import SummarizeJob
from tgen.jobs.summary_jobs.summary_response import SummaryResponse


def perform_summarize_request(data: SummarizeRequest) -> SummaryResponse:
    """
    Performs artifact summarization.
    :param data: Serialized data.
    :return: The same artifacts with content as summary.
    """
    dataset_creator = create_api_dataset(data.artifacts, project_summary=data.project_summary)
    summarize_job = SummarizeJob(dataset_creator=dataset_creator)
    summary_response = ViewUtil.run_job(summarize_job)
    return summary_response


@endpoint(SummarizeSerializer)
def perform_summarization_sync(request_data: SummarizeRequest):
    """
    Summarizes dataset artifacts synchronously
    :param request_data: The data containing dataset to summarize.
    :return: Summary output.
    """
    return perform_summarize_request(request_data)


@endpoint(SummarizeSerializer, is_async=True)
def perform_summarization_job(request_data: SummarizeRequest):
    """
    Summarizes dataset using a job.
    :param request_data: The dataset containing artifacts to summarize.
    :return:
    """
    return perform_summarize_request(request_data)
