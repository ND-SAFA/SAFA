import os
from typing import Optional

from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.tools.constants.symbol_constants import EMPTY_STRING
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.file_util import FileUtil

from tgen.clustering.base.cluster_type import ClusterIdType, ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.project_summary_constants import MAX_ITERATIONS_ALLOWED, MAX_TOKENS_FOR_PROJECT_SUMMARY
from tgen.common.util.pipeline_util import nested_pipeline
from tgen.models.tokens.token_calculator import TokenCalculator
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summarizer_state import SummarizerState


class StepCreateArtifactBatches(AbstractPipelineStep[SummarizerArgs, SummarizerState]):

    def _run(self, args: SummarizerArgs, state: SummarizerState) -> None:
        """
        Creates clusters from artifacts to generate new project summary form.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :return: None
        """
        cluster_map = {0: list(state.dataset.artifact_df.index)}
        final_cluster_map = self.cluster_until_prompt_fits(cluster_map, state.dataset.artifact_df, args.export_dir)
        state.batch_id_to_artifacts = final_cluster_map

    @staticmethod
    def cluster_until_prompt_fits(initial_cluster_map: ClusterIdType, artifact_df: ArtifactDataFrame, export_dir: str):
        """
        Recursively clusters ones exceeding size limit.
        :param initial_cluster_map: Map of ID to cluster to check.
        :param artifact_df: Artifact DataFrame containing all artifacts referenced in clusters.
        :param export_dir: Optional export directory to save state in.
        :return: Final cluster map.
        """
        cluster_map = {**initial_cluster_map}
        n_iterations = 0
        while True:
            large_cluster_map = StepCreateArtifactBatches.extract_large_clusters(cluster_map,
                                                                                 artifact_df,
                                                                                 MAX_TOKENS_FOR_PROJECT_SUMMARY)
            if len(large_cluster_map) == 0:
                break

            for cluster_id, _ in large_cluster_map.items():
                cluster_map.pop(cluster_id)
            large_cluster_mini_batches = StepCreateArtifactBatches.create_mini_clusters(large_cluster_map, export_dir)
            cluster_map.update(large_cluster_mini_batches)
            n_iterations += 1

            if n_iterations > MAX_ITERATIONS_ALLOWED:
                logger.warning("Clustering for project summary has reached the maximum number of iterations")
                break
        return cluster_map

    @staticmethod
    def extract_large_clusters(cluster_map: ClusterIdType, artifact_df: ArtifactDataFrame, token_limit: int) -> ClusterIdType:
        """
        Extracts clusters in map exceeding
        :param cluster_map: Map ID to cluster to access if is larger than expected.
        :param artifact_df: DataFrame containing artifacts in clusters.
        :param token_limit: The maximum number of tokens allowable per cluster.
        :return: Cluster map of large clusters.
        """
        curr_items = list(cluster_map.items())
        large_clusters = {}
        for cluster_id, cluster_artifacts in curr_items:
            cluster_artifact_df = artifact_df.filter_by_index(cluster_artifacts)
            cluster_artifact_contents = cluster_artifact_df.get_summaries_or_contents(cluster_artifacts)
            cluster_content = EMPTY_STRING.join(cluster_artifact_contents)
            n_tokens = TokenCalculator.estimate_num_tokens(cluster_content)
            if n_tokens > token_limit:
                large_clusters[cluster_id] = (cluster_artifact_df, n_tokens)
        return large_clusters

    @staticmethod
    def create_mini_clusters(cluster_map: ClusterIdType, export_dir: Optional[str]) -> ClusterIdType:
        """
        Creates mini-clusters for each cluster in map.
        :param cluster_map: Map of cluster id to cluster to create mini-clusters for.
        :param export_dir: Path to direction to store state.
        :return: Map of mini-cluster id to artifacts in mini-cluster.
        """
        mini_batch_map = {}
        for parent_cluster_id, (cluster_artifact_df, cluster_tokens) in cluster_map.items():
            cluster_export_dir = os.path.join(export_dir, str(parent_cluster_id)) if export_dir else None
            cluster_mini_batches = StepCreateArtifactBatches._run_clustering_pipeline(cluster_artifact_df,
                                                                                      cluster_tokens,
                                                                                      export_dir=cluster_export_dir)
            cluster_mini_batches = {f"{parent_cluster_id}:{c_id}": c_artifacts
                                    for c_id, c_artifacts in cluster_mini_batches.items()}
            mini_batch_map.update(cluster_mini_batches)
        return mini_batch_map

    @staticmethod
    @nested_pipeline(SummarizerState)
    def _run_clustering_pipeline(artifact_df: ArtifactDataFrame, n_tokens: int, export_dir: str = None) -> ClusterMapType:
        """
        Runs the clustering pipeline to break the project into clusters.
        :param artifact_df: The artifacts to cluster.
        :param export_dir: Where to export state to.
        :param n_tokens: The number of tokens in the content of the project.
        :return: The cluster map from the pipeline.
        """
        dataset = PromptDataset(artifact_df=artifact_df)
        n_artifacts = len(dataset.artifact_df)
        avg_file_size = n_tokens / n_artifacts
        max_cluster_size = round(MAX_TOKENS_FOR_PROJECT_SUMMARY / avg_file_size)
        min_cluster_size = round(min(.25 * n_artifacts, (MAX_TOKENS_FOR_PROJECT_SUMMARY / avg_file_size) * .75))
        clustering_export_path = FileUtil.safely_join_paths(export_dir, "clustering")
        cluster_args = ClusteringArgs(dataset=dataset, create_dataset=True, export_dir=clustering_export_path,
                                      cluster_min_size=min_cluster_size,
                                      cluster_max_size=max_cluster_size,
                                      filter_by_cohesiveness=False,
                                      add_orphans_to_best_home=True)
        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()
        cluster_map = clustering_pipeline.state.final_cluster_map
        return {cluster_id: cluster for cluster_id, cluster in cluster_map.items() if len(cluster) > 1}
