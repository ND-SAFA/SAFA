from typing import List

from rest_framework.views import APIView

from api.endpoints.hgen.hgen_serializer import HGenSerializer
from api.endpoints.predict.prediction_view import endpoint
from api.utils.model_util import ModelUtil
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.hgen_jobs.artifact_generator_job import ArtifactGeneratorJob

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
        prompt = payload.get("prompt", DEFAULT_PROMPT)
        artifacts = payload["artifacts"]
        clusters = payload["clusters"]
        model, llm_manager = ModelUtil.get_model_manager(model)
        summarizer = Summarizer(code_or_exceeds_limit_only=True, llm_manager=llm_manager)
        job = ArtifactGeneratorJob(artifacts,
                                   artifact_ids_by_cluster=clusters,
                                   llm_manager=llm_manager,
                                   hgen_base_prompt=prompt,
                                   summarizer=summarizer)

        def post_process(summarized_artifact: List[str]):
            return {"artifacts": summarized_artifact}

        return job, post_process
