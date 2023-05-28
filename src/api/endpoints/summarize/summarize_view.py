from api.endpoints.base.views.endpoint import async_endpoint
from api.endpoints.summarize.summarize_serializer import SummarizePayload, SummarizeSerializer
from api.utils.view_util import ViewUtil
from tgen.constants.model_constants import get_default_llm_manager
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob


@async_endpoint(SummarizeSerializer)
def perform_summarization(request_data: SummarizePayload):
    """
    Performs artifact summarization.
    :param request_data: Serialized data.
    :return: The same artifacts with content as summary.
    """
    artifacts = request_data["artifacts"]
    job_args = JobArgs()
    llm_manager = get_default_llm_manager()
    llm_manager.llm_args.temperature = 0.5

    summarizer = Summarizer(llm_manager, code_or_exceeds_limit_only=False)
    summarize_job = SummarizeArtifactsJob(artifacts, job_args=job_args, summarizer=summarizer)

    summarized_artifacts = ViewUtil.run_job(summarize_job)
    return {"artifacts": summarized_artifacts}
