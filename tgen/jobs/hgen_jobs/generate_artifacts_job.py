from typing import List, Union

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.hgen_jobs.base_hgen_job import BaseHGenJob
from tgen.util.enum_util import EnumDict


class GenerateArtifactsJob(BaseHGenJob):
    SOURCE_LAYER_ID = "source_layer"

    def __init__(self, artifacts: List[EnumDict], target_type: str, artifact_ids_by_cluster: List[List[Union[str, int]]] = None,
                 job_args: JobArgs = None, **hgen_params):
        """
        Initializes the job with args needed for hierarchy generator
        :param artifacts: A dictionary mapping artifact id to a dictionary containing its content and type (e.g. java, py, nl)
        :param artifact_ids_by_cluster: A list of lists of artifact ids representing each cluster
        :param target_type: The type of higher-level artifact that will be generated
        :param llm_manager: Model Manager in charge of generating artifacts
        :param summarizer: Used to summarize the source artifacts
        :param job_args: The arguments need for the job
        :param hgen_params: Any additional parameters for the hgen args
        """
        artifacts = [EnumDict(a) for a in artifacts]
        self.artifacts = artifacts
        self.target_type = target_type
        self.artifacts_by_cluster = artifact_ids_by_cluster if artifact_ids_by_cluster is not None else {}
        super().__init__(job_args=job_args, **hgen_params)

    def get_hgen_args(self) -> HGenArgs:
        """
        Gets the arguments used for the hierarchy generation
        :return: The arguments used for the hierarchy generation
        """
        args = HGenArgs(dataset_for_sources=self._create_dataset(),
                        source_layer_id=self.SOURCE_LAYER_ID,
                        target_type=self.target_type,
                        **self.hgen_params)
        return args

    def _create_dataset(self) -> PromptDataset:
        """
        Creates a trace dataset containing the given artifacts
        :return: The trace dataset containing the artifacts
        """
        artifacts_dict = [EnumDict({ArtifactKeys.ID: artifact[ArtifactKeys.ID],
                                    ArtifactKeys.CONTENT: artifact[ArtifactKeys.CONTENT],
                                    ArtifactKeys.LAYER_ID: GenerateArtifactsJob.SOURCE_LAYER_ID})
                          for artifact in self.artifacts]
        return PromptDataset(artifact_df=ArtifactDataFrame(artifacts_dict))
