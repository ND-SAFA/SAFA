from api.endpoints.common.dataset_converter import create_api_dataset
from api.endpoints.common.endpoint_decorator import endpoint
from api.endpoints.serializers.hgen_serializer import HGenRequest, HGenSerializer
from api.utils.view_util import ViewUtil
from tgen.common.constants.project_summary_constants import PS_FEATURE_TITLE
from tgen.common.logging.logger_manager import logger
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.hgen.hgen_args import HGenArgs
from tgen.jobs.hgen_jobs.base_hgen_job import BaseHGenJob
from tgen.jobs.hgen_jobs.multi_layer_hgen_job import MultiLayerHGenJob

ARTIFACT_LAYER = "source_layer_id"


@endpoint(HGenSerializer, is_async=True)
def perform_hgen(request: HGenRequest):
    """
    Performs generation of single artifacts from cluster.
    :param request: The request containing cluster of artifacts to summarize.
    :return: The generated artifact(s).
    """
    artifacts = list(filter(lambda a: a[ArtifactKeys.CONTENT], request.artifacts))
    target_types = request.target_types
    source_layer_ids = list(set([a[ArtifactKeys.LAYER_ID] for a in artifacts]))

    seed_title_section = None if len(artifacts) <= 10 else PS_FEATURE_TITLE

    summary = request.summary
    base_type, *other_types = target_types
    logger.info(f"Starting HGEN request for: {target_types}")
    dataset_creator = create_api_dataset(artifacts, project_summary=summary)
    hgen_args = HGenArgs(source_layer_ids=source_layer_ids,
                         target_type=base_type,
                         dataset_creator=dataset_creator,
                         seed_project_summary_section=seed_title_section)
    base_job = BaseHGenJob(hgen_args)
    job = MultiLayerHGenJob(base_job,
                            target_types=other_types)
    hgen_dataset = ViewUtil.run_job(job)
    return hgen_dataset
