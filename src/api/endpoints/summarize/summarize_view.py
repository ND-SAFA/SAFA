from celery import shared_task

from api.endpoints.base.views.endpoint import endpoint
from api.endpoints.summarize.summarize_serializer import SummarizePayload, SummarizeSerializer
from api.utils.model_util import ModelUtil
from api.utils.view_util import ViewUtil
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob


@endpoint(SummarizeSerializer)
@shared_task
def perform_summarization(request_data: SummarizePayload):
    """
    Performs artifact summarization.
    :param request_data: Serialized data.
    :return: The same artifacts with content as summary.
    """
    artifacts = request_data["artifacts"]
    llm_name = request_data.get("model", ModelUtil.get_default_model())
    job_args = JobArgs()
    model, llm_manager = ModelUtil.get_model_manager(llm_name)
    llm_manager.llm_args.temperature = 0.25

    summarizer = Summarizer(llm_manager, code_or_exceeds_limit_only=False)
    summarize_job = SummarizeArtifactsJob(artifacts, job_args=job_args, summarizer=summarizer)

    summarized_artifacts = ViewUtil.run_job(summarize_job)
    return {"artifacts": summarized_artifacts}
