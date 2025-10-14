import os
import shutil
import uuid

from api.cloud.s3_util import upload_to_s3
from api.endpoints.gen.hgen.hgen_serializer import HGenRequest, HGenSerializer
from api.endpoints.handler.dataset_converter import create_api_dataset
from api.endpoints.handler.endpoint_decorator import endpoint
from api.server.settings import ENV_FAILURE_PATH, ENV_NAME
from api.utils.view_util import ViewUtil
from gen.hgen.hgen_args import HGenArgs
from gen.hgen.jobs.multi_layer_hgen_job import MultiLayerHGenJob
from gen_common.constants.summary_constants import PS_SUBSYSTEM_TITLE

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

    seed_title_section = None if len(artifacts) <= 10 else PS_SUBSYSTEM_TITLE

    summary = request.summary
    base_type, *other_types = target_types
    run_id = uuid.uuid4()

    cloud_emergency_path = os.path.join("failures", ENV_NAME, str(run_id) + ".zip")
    local_emergency_path = os.path.expanduser(os.path.join(ENV_FAILURE_PATH, "failures", str(run_id)))

    logger.info(f"Starting HGEN request for: {target_types}")  #
    dataset_creator = create_api_dataset(artifacts, project_summary=summary)
    hgen_args = HGenArgs(source_layer_ids=source_layer_ids,
                         target_type=base_type,
                         dataset_creator=dataset_creator,
                         seed_project_summary_section=seed_title_section)
    base_job = BaseHGenJob(hgen_args)
    job = MultiLayerHGenJob(base_job,
                            target_types=other_types,
                            save_on_failure_path=local_emergency_path)
    hgen_dataset = ViewUtil.run_job(job, on_failure=lambda: on_job_failure(local_emergency_path, cloud_emergency_path))
    return hgen_dataset


def on_job_failure(local_emergency_path: str, cloud_emergency_path: str):
    """
    Zips input folder, uploads to s3, and deletes local files.
    :param local_emergency_path:
    :param cloud_emergency_path:
    :return:
    """
    assert ".zip" in cloud_emergency_path, f"Expected .zip in {cloud_emergency_path}"

    dir_name = os.path.dirname(local_emergency_path)
    zip_file_path = os.path.join(dir_name, 'temp')
    shutil.make_archive(zip_file_path, "zip", local_emergency_path)
    output_path = f"{zip_file_path}.zip"

    upload_to_s3(output_path, cloud_emergency_path)
    shutil.rmtree(local_emergency_path)
    os.remove(output_path)
    logger.info(f"Successfully saved state of failed job to: {cloud_emergency_path}")
