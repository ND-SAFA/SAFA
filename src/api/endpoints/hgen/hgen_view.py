from api.endpoints.base.views.endpoint import async_endpoint
from api.endpoints.hgen.hgen_serializer import HGenSerializer
from api.utils.view_util import ViewUtil
from tgen.jobs.hgen_jobs.generate_artifacts_job import GenerateArtifactsJob


@async_endpoint(HGenSerializer)
def perform_hgen(payload):
    """
    Performs generation of single artifacts from cluster.
    :param payload: The request containing cluster of artifacts to summarize.
    :return: The generated artifact(s).
    """
    print("PAYLOAD")
    print(payload)
    print("\n\n")
    target_type = payload["targetType"]
    artifacts = payload["artifacts"]
    clusters = payload.get("clusters", None)
    job = GenerateArtifactsJob(artifacts,
                               artifact_ids_by_cluster=clusters,
                               target_type=target_type)

    hgen_dataset = ViewUtil.run_job(job)
    return {"dataset": hgen_dataset}
