import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from api.utils.model_util import ModelUtil
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob
from tgen.util.json_util import NpEncoder
from tgen.util.status import Status


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
        request_data = json.loads(request.body)
        artifacts = request_data["artifacts"]
        llm_name = request_data.get("model", ModelUtil.get_default_model())
        job_args = JobArgs()
        model, llm_manager = ModelUtil.get_model_manager(llm_name)

        summarizer = Summarizer(llm_manager, code_or_exceeds_limit_only=False)
        summarize_job = SummarizeArtifactsJob(artifacts, job_args=job_args, summarizer=summarizer)
        job_result = summarize_job.run()
        
        job_body = job_result.to_json(as_dict=True)["body"]
        if job_result.status == Status.FAILURE:
            return JsonResponse(job_body, status=400)
        return JsonResponse({"body": {"artifacts": job_body}}, encoder=NpEncoder)
