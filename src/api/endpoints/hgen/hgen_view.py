from typing import List

from rest_framework.views import APIView

from api.endpoints.hgen.hgen_serializer import HGenSerializer
from api.endpoints.predict.prediction_view import endpoint
from api.utils.model_util import ModelUtil
from tgen.jobs.hgen_jobs.generate_artifacts_job import GenerateArtifactsJob

DEFAULT_PROMPT = "Generalize the following descriptions into one system requirement.\n\n{}"


class HGenView(APIView):
    """"
    Provides endpoint for generating artifacts.
    """

    @endpoint(HGenSerializer)
    def post(self, payload):
        """
        Performs generation of single artifacts from cluster.
        :param payload: The request containing cluster of artifacts to summarize.
        :return: The generated artifact(s).
        """
        model = payload.get("model", ModelUtil.get_default_model())
        target_type = payload["targetType"]
        artifacts = payload["artifacts"]
        clusters = payload.get("clusters", None)
        model, llm_manager = ModelUtil.get_model_manager(model)
        job = GenerateArtifactsJob(artifacts,
                                   artifact_ids_by_cluster=clusters,
                                   llm_manager=llm_manager,
                                   target_type=target_type)

        def post_process(summarized_artifact: List[str]):
            return {"dataset": summarized_artifact}

        return job, post_process
