from django.http import HttpRequest, JsonResponse
from rest_framework.views import APIView

from api.endpoints.hgen.hgen_serializer import HGenSerializer
from api.utils.model_util import ModelUtil
from api.utils.view_util import ViewUtil
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.hgen_jobs.artifact_generator_job import ArtifactGeneratorJob

DEFAULT_PROMPT = "Generalize the following descriptions into one system requirement.\n\n{}"


class HGenView(APIView):
    """"
    Provides endpoint for generating artifacts.
    """

    def post(self, request: HttpRequest):
        """
        Performs generation of single artifacts from cluster.
        :param request: The request containing cluster of artifacts to summarize.
        :return: The generated artifact(s).
        """
        request = ViewUtil.read_request(request, HGenSerializer)
        model = request.get("model", ModelUtil.get_default_model())
        prompt = request.get("prompt", DEFAULT_PROMPT)
        model, llm_manager = ModelUtil.get_model_manager(model)
        job = ArtifactGeneratorJob(request[JobResult.ARTIFACTS], artifact_ids_by_cluster=request["clusters"],
                                   llm_manager=llm_manager, hgen_base_prompt=prompt)
        response = job.run()
        artifacts = response[JobResult.ARTIFACTS]
        return JsonResponse({JobResult.ARTIFACTS: artifacts})
