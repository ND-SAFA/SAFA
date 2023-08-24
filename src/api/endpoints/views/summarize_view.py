from api.endpoints.base.endpoint import async_endpoint, endpoint
from api.endpoints.serializers.summarize_serializer import SummarizeRequest, SummarizeSerializer
from api.utils.view_util import ViewUtil
from tgen.jobs.summary_jobs.summarize_artifacts_job import SummarizeArtifactsJob


@endpoint(SummarizeSerializer)
def perform_summarization_sync(request_data: SummarizeRequest):
    return perform_summarize_request(request_data)


@async_endpoint(SummarizeSerializer)
def perform_summarization_job(request_data: SummarizeRequest):
    return perform_summarize_request(request_data)


LAYER_ID = "SUMMARIZE_LAYER_ID"


def perform_summarize_request(data: SummarizeRequest):
    """
    Performs artifact summarization.
    :param data: Serialized data.
    :return: The same artifacts with content as summary.
    """
    summarize_job = SummarizeArtifactsJob(data.artifacts,
                                          project_summary=data.project_summary,
                                          do_resummarize_project=False,
                                          is_subset=True)

    summarized_artifacts = ViewUtil.run_job(summarize_job)
    return summarized_artifacts
