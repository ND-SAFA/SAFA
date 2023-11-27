from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.project_summary_constants import MAX_TOKENS_FOR_PROJECT_SUMMARY
from tgen.common.util.file_util import FileUtil
from tgen.models.tokens.token_calculator import TokenCalculator
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.common.util.pipeline_util import nested_pipeline
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summarizer_state import SummarizerState
from tgen.summarizer.summarizer_util import SummarizerUtil


class StepClusterArtifacts(AbstractPipelineStep[SummarizerArgs, SummarizerState]):

    def _run(self, args: SummarizerArgs, state: SummarizerState) -> None:
        """
        Creates clusters from artifacts to generate new project summary form.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :return: None
        """
        all_content = EMPTY_STRING.join(state.dataset.artifact_df.get_summaries_or_contents())
        n_tokens = TokenCalculator.estimate_num_tokens(all_content)
        if n_tokens < MAX_TOKENS_FOR_PROJECT_SUMMARY or not SummarizerUtil.needs_project_summary(state.dataset.project_summary, args):
            state.cluster_id_to_artifacts = {0: list(state.dataset.artifact_df.index)}
            return

        final_cluster_map = self._run_clustering_pipeline(args, state, n_tokens)

        state.cluster_id_to_artifacts = {cluster_id: cluster.artifact_ids for cluster_id, cluster in final_cluster_map.items()}

    @nested_pipeline(SummarizerState)
    def _run_clustering_pipeline(self, args: SummarizerArgs, state: SummarizerState, n_tokens: int) -> ClusterMapType:
        """
        Runs the clustering pipeline to break the project into clusters.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :param n_tokens: The number of tokens in the content of the project.
        :return: The cluster map from the pipeline.
        """
        n_artifacts = len(state.dataset.artifact_df)
        avg_file_size = n_tokens / n_artifacts
        max_cluster_size = round(MAX_TOKENS_FOR_PROJECT_SUMMARY / avg_file_size)
        min_cluster_size = round(min(.25 * n_artifacts, (MAX_TOKENS_FOR_PROJECT_SUMMARY / avg_file_size) * .75))
        cluster_reduction_factor = 1 / max_cluster_size
        clustering_export_path = FileUtil.safely_join_paths(args.export_dir, "clustering")
        cluster_args = ClusteringArgs(dataset=state.dataset, create_dataset=True, export_dir=clustering_export_path,
                                      cluster_reduction_factor=cluster_reduction_factor,
                                      cluster_min_size=min_cluster_size,
                                      cluster_max_size=max_cluster_size,
                                      filter_by_cohesiveness=False,
                                      add_orphans_to_best_home=True)
        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()
        cluster_map = clustering_pipeline.state.final_cluster_map
        return {cluster_id: cluster for cluster_id, cluster in cluster_map.items() if len(cluster) > 1}
