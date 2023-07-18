from api.endpoints.base.views.endpoint import async_endpoint
from api.endpoints.hgen.hgen_serializer import HGenRequest, HGenSerializer
from api.utils.view_util import ViewUtil
from tgen.jobs.hgen_jobs.generate_artifacts_job import GenerateArtifactsJob
from tgen.jobs.hgen_jobs.multi_layer_hgen_job import MultiLayerHGenJob
from tgen.util.logging.logger_manager import logger


@async_endpoint(HGenSerializer)
def perform_hgen(request: HGenRequest):
    """
    Performs generation of single artifacts from cluster.
    :param request: The request containing cluster of artifacts to summarize.
    :return: The generated artifact(s).
    """
    artifacts = request["artifacts"]
    target_types = request["targetTypes"]
    summary = request.get("summary")
    base_type, *other_types = target_types
    logger.info(f"Starting HGEN request for: {target_types}")
    base_job = GenerateArtifactsJob(artifacts,
                                    target_type=base_type,
                                    system_summary=summary)
    job = MultiLayerHGenJob(base_job,
                            target_types=other_types)
    hgen_dataset = ViewUtil.run_job(job)
    return hgen_dataset
