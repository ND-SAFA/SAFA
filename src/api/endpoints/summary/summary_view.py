from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from api.endpoints.summary.summary_serializer import SummarySerializer
from api.utils.model_util import ModelUtil
from api.utils.view_util import ViewUtil
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob
from tgen.util.json_util import NpEncoder


class SummaryView(APIView):
    """
    Provides endpoint for summarizing artifacts.
    """

    @csrf_exempt
    def post(self, request: HttpRequest):
        """
        Performs artifact summarization.
        :param request: Request containing artifacts to summarize.
        :return: The same artifacts with content as summary.
        """
        request_data = ViewUtil.read_request(request, SummarySerializer)
        artifacts = request_data["artifacts"]
        llm_name = request_data.get("model", ModelUtil.get_default_model())
        job_args = JobArgs()
        model, llm_manager = ModelUtil.get_model_manager(llm_name)

        summarizer = Summarizer(llm_manager)
        summarize_job = SummarizeArtifactsJob(artifacts, job_args=job_args, summarizer=summarizer)
        summarized_artifacts = summarize_job.run()[JobResult.ARTIFACTS]
        return JsonResponse({"artifacts": summarized_artifacts}, encoder=NpEncoder)
