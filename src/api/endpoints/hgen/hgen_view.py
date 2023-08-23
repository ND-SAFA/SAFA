from typing import List

from api.endpoints.base.views.endpoint import async_endpoint
from api.endpoints.hgen.hgen_serializer import HGenRequest, HGenSerializer
from api.endpoints.summarize.summarize_serializer import SummaryArtifactPayload
from api.utils.view_util import ViewUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.logging.logger_manager import logger
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.readers.abstract_project_reader import AbstractProjectReader, ProjectData
from tgen.hgen.hgen_args import HGenArgs
from tgen.jobs.hgen_jobs.base_hgen_job import BaseHGenJob
from tgen.jobs.hgen_jobs.multi_layer_hgen_job import MultiLayerHGenJob

ARTIFACT_LAYER = "source_layer_id"


class SummaryArtifactProjectReader(AbstractProjectReader):
    def __init__(self, artifacts: List):
        super().__init__()
        self.artifacts = artifacts

    def read_project(self) -> ProjectData:
        def convert_to_artifact(a: SummaryArtifactPayload):
            a_dict = {ArtifactKeys.ID: a["id"], ArtifactKeys.CONTENT: a["content"], ArtifactKeys.LAYER_ID: ARTIFACT_LAYER}
            return EnumDict(a_dict)

        artifacts = [convert_to_artifact(a) for a in self.artifacts]
        artifact_df = ArtifactDataFrame(artifacts)
        layer_df = LayerDataFrame()
        trace_df = TraceDataFrame()
        return artifact_df, trace_df, layer_df

    def get_project_name(self) -> str:
        return "api"


@async_endpoint(HGenSerializer)
def perform_hgen(request: HGenRequest):
    """
    Performs generation of single artifacts from cluster.
    :param request: The request containing cluster of artifacts to summarize.
    :return: The generated artifact(s).
    """
    artifacts = request["artifacts"]
    target_types = request["targetTypes"]
    summary = request.get("summary", None)
    base_type, *other_types = target_types
    logger.info(f"Starting HGEN request for: {target_types}")
    trace_dataset_creator = TraceDatasetCreator(SummaryArtifactProjectReader(artifacts=artifacts))
    dataset_creator = PromptDatasetCreator(trace_dataset_creator=trace_dataset_creator)
    hgen_args = HGenArgs(source_layer_id=ARTIFACT_LAYER,
                         target_type=base_type,
                         dataset_creator_for_sources=dataset_creator,
                         system_summary=summary)
    base_job = BaseHGenJob(hgen_args)
    job = MultiLayerHGenJob(base_job,
                            target_types=other_types)
    hgen_dataset = ViewUtil.run_job(job)
    return hgen_dataset
