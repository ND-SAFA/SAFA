from api.endpoints.base.views.endpoint import async_endpoint, endpoint
from api.endpoints.summarize.summarize_serializer import SummarizePayload, SummarizeSerializer
from api.utils.view_util import ViewUtil
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.train.args.anthropic_args import AnthropicArgs


@endpoint(SummarizeSerializer)
def perform_summarization_sync(request_data: SummarizePayload):
    return perform_summarize_request(request_data)


@async_endpoint(SummarizeSerializer)
def perform_summarization_job(request_data: SummarizePayload):
    return perform_summarize_request(request_data)


def perform_summarize_request(request_data: SummarizePayload):
    """
    Performs artifact summarization.
    :param request_data: Serialized data.
    :return: The same artifacts with content as summary.
    """
    artifacts = request_data.artifacts
    job_args = JobArgs()
    llm_args = AnthropicArgs(model="claude-instant-1.1", temperature=0.25)
    llm_manager = AnthropicManager(llm_args=llm_args)
    summarizer = Summarizer(llm_manager=llm_manager, code_or_exceeds_limit_only=False)
    summarize_job = SummarizeArtifactsJob(artifacts, job_args=job_args, summarizer=summarizer)

    summarized_artifacts = ViewUtil.run_job(summarize_job)
    return {"artifacts": summarized_artifacts}
