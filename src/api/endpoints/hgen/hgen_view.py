from celery import shared_task

from api.endpoints.base.views.endpoint import endpoint
from api.endpoints.hgen.hgen_serializer import HGenSerializer
from api.utils.model_util import ModelUtil
from api.utils.view_util import ViewUtil
from tgen.jobs.hgen_jobs.generate_artifacts_job import GenerateArtifactsJob


@endpoint(HGenSerializer)
@shared_task
def perform_hgen(payload):
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

    hgen_dataset = ViewUtil.run_job(job)
    return {"dataset": hgen_dataset}
