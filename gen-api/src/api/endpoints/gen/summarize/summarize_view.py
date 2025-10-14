from api.endpoints.gen.summarize.summarize_serializer import SummarizeRequest, SummarizeSerializer
from api.endpoints.handler.dataset_converter import create_api_dataset
from api.endpoints.handler.endpoint_decorator import endpoint
from api.utils.view_util import ViewUtil
from gen.summary.summarize_job import SummarizeJob
from gen.summary.summary_response import SummaryResponse
from gen_common.jobs.job_args import JobArgs


def perform_summarize_request(data: SummarizeRequest, **kwargs) -> SummaryResponse:
    """
    Performs artifact summarization.
    :param data: Serialized data.
    :return: The same artifacts with content as summary.
    """
    dataset_creator = create_api_dataset(data.artifacts, project_summary=data.project_summary)
    job_args = JobArgs(dataset_creator=dataset_creator)
    summarize_job = SummarizeJob(job_args, **kwargs)
    summary_response = ViewUtil.run_job(summarize_job)
    return summary_response


@endpoint(SummarizeSerializer)
def perform_summarization_sync(request_data: SummarizeRequest):
    """
    Summarizes dataset artifacts synchronously
    :param request_data: The data containing dataset to summarize.
    :return: Summary output.
    """
    return perform_summarize_request(request_data, project_summary_sections=[], summarize_code_only=False)


@endpoint(SummarizeSerializer, is_async=True)
def perform_summarization_job(request_data: SummarizeRequest):
    """
    Summarizes dataset using a job.
    :param request_data: The dataset containing artifacts to summarize.
    :return:
    """
    return perform_summarize_request(request_data)
