from typing import Dict, List, Union

from tgen.data.creators.clustering.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.creators.clustering.supported_clustering_method import SupportedClusteringMethod
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob
from tgen.jobs.hgen_jobs.hgen_job import HGenJob
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.util.enum_util import EnumDict
from tgen.util.override import overrides
from tgen.util.status import Status


class ArtifactGeneratorJob(HGenJob):
    SOURCE_LAYER_ID = "source_layer"

    def __init__(self, artifacts: Dict[str, Dict], artifact_ids_by_cluster: List[List[Union[str, int]]],
                 llm_manager: AbstractLLMManager, hgen_base_prompt: Union[str, SupportedPrompts],
                 summarizer: Summarizer = None, job_args: JobArgs = None):
        """
        Initializes the job with args needed for hierarchy generator
        :param artifacts: A dictionary mapping artifact id to a dictionary containing its content and type (e.g. java, py, nl)
        :param artifact_ids_by_cluster: A list of lists of artifact ids representing each cluster
        :param hgen_base_prompt: The base prompt used to create the artifacts
        :param llm_manager: Model Manager in charge of generating artifacts
        :pram job_args: The arguments need for the job
        """
        self.artifacts = self._summarize_artifacts(artifacts, summarizer, job_args)
        self.artifacts_by_cluster = artifact_ids_by_cluster
        trace_dataset = self._create_trace_dataset_from_artifacts(self.artifacts)
        dataset_creator = ClusterDatasetCreator(trace_dataset=trace_dataset,
                                                manual_clusters={i: artifacts_in_cluster
                                                                 for i, artifacts_in_cluster in enumerate(self.artifacts_by_cluster)})
        hgen_args = HGenArgs(source_layer_id=self.SOURCE_LAYER_ID, hgen_base_prompt=hgen_base_prompt,
                             dataset_creator_for_clusters=dataset_creator, cluster_method=SupportedClusteringMethod.MANUAL)
        super().__init__(hgen_args=hgen_args, llm_manager=llm_manager, job_args=job_args)

    @overrides(HGenJob)
    def _run(self) -> List[str]:
        """
        Converts output of HGenJob to a list of the cluster content
        :return: The job result containing the list of cluster content
        """
        generated_dataset: TraceDataset = super()._run()
        artifacts = [artifact[ArtifactKeys.CONTENT] for id_, artifact in generated_dataset.artifact_df.itertuples()
                     if artifact[ArtifactKeys.LAYER_ID] != self.SOURCE_LAYER_ID]
        return artifacts

    @staticmethod
    def _create_trace_dataset_from_artifacts(artifacts: Dict[str, Dict]) -> TraceDataset:
        """
        Creates a trace dataset containing the given artifacts
        :param artifacts: The artifacts used for the generation
        :return: The trace dataset containing the artifacts
        """
        artifacts = [EnumDict({ArtifactKeys.ID: id_,
                               ArtifactKeys.CONTENT: artifact[ArtifactKeys.CONTENT.value],
                               ArtifactKeys.LAYER_ID: ArtifactGeneratorJob.SOURCE_LAYER_ID}) for id_, artifact in artifacts.items()]
        artifact_df = ArtifactDataFrame(artifacts)
        trace_dataset = TraceDataset(artifact_df, TraceDataFrame(), LayerDataFrame())
        return trace_dataset

    @staticmethod
    def _summarize_artifacts(artifacts: Dict[str, Dict], summarizer: Summarizer, job_args: JobArgs) -> Dict[str, Dict]:
        """
        Runs summarize job on artifacts
        :param artifacts: The artifacts to summarize
        :param summarizer: The summarizer to use
        :param job_args: Any job args for the job
        :return: The summarized artifacts
        """
        summarize_job = SummarizeArtifactsJob(artifacts, job_args=job_args,
                                              summarizer=summarizer if summarizer is not None else
                                              Summarizer(code_or_exceeds_limit_only=True))
        job_result = summarize_job.run()
        if job_result.status == Status.FAILURE:
            raise Exception(job_result.body)
        return job_result.body
