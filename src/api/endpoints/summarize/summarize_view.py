from api.endpoints.base.views.endpoint import async_endpoint, endpoint
from api.endpoints.summarize.summarize_serializer import SummarizeRequest, SummarizeSerializer
from api.utils.view_util import ViewUtil
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.summary_jobs.summarize_artifacts_job import SummarizeArtifactsJob


@endpoint(SummarizeSerializer)
def perform_summarization_sync(request_data: SummarizeRequest):
    return perform_summarize_request(request_data)


@async_endpoint(SummarizeSerializer)
def perform_summarization_job(request_data: SummarizeRequest):
    return perform_summarize_request(request_data)


LAYER_ID = "SUMMARIZE_LAYER_ID"


def perform_summarize_request(request_data: SummarizeRequest):
    """
    Performs artifact summarization.
    :param request_data: Serialized data.
    :return: The same artifacts with content as summary.
    """
    artifacts = [EnumDict({
        ArtifactKeys.ID: a["id"],
        ArtifactKeys.CONTENT: a["content"],
        ArtifactKeys.LAYER_ID: LAYER_ID
    }) for a in request_data.artifacts]
    job_args = JobArgs()
    summarize_job = SummarizeArtifactsJob(artifacts, job_args=job_args, is_subset=True)

    summarized_artifacts = ViewUtil.run_job(summarize_job)
    return summarized_artifacts
