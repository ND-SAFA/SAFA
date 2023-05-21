from rest_framework.views import APIView

from api.endpoints.base.views.endpoint import endpoint
from api.endpoints.summarize.summarize_serializer import SummarizeSerializer
from api.utils.model_util import ModelUtil
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob


class SummarizeView(APIView):
    """
    Provides endpoint for summarizing artifacts.
    """

    @endpoint(SummarizeSerializer)
    def post(self, request_data):
        """
        Performs artifact summarization.
        :param request_data: Serialized data.
        :return: The same artifacts with content as summary.
        """
        artifacts = request_data["artifacts"]
        llm_name = request_data.get("model", ModelUtil.get_default_model())
        job_args = JobArgs()
        model, llm_manager = ModelUtil.get_model_manager(llm_name)

        summarizer = Summarizer(llm_manager, code_or_exceeds_limit_only=False)
        summarize_job = SummarizeArtifactsJob(artifacts, job_args=job_args, summarizer=summarizer)

        def post_process(job_body):
            return {"artifacts": job_body}

        return summarize_job, post_process
