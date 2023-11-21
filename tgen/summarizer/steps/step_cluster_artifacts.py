from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.project_summary_constants import MAX_TOKENS_FOR_PROJECT_SUMMARY
from tgen.common.util.file_util import FileUtil
from tgen.models.tokens.token_calculator import TokenCalculator
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
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
        if n_tokens < MAX_TOKENS_FOR_PROJECT_SUMMARY or not SummarizerUtil.needs_project_summary(state.dataset, args):
            state.cluster_map = {0: Cluster.from_artifact_map(state.dataset.artifact_df.to_map(), update_stats=False)}
            return

        cluster_reduction_factor = 0.5  # TODO
        clustering_export_path = FileUtil.safely_join_paths(args.export_dir, "clustering")
        cluster_args = ClusteringArgs(dataset=state.dataset, create_dataset=True, export_dir=clustering_export_path,
                                      cluster_reduction_factor=cluster_reduction_factor,
                                      cluster_min_size=1,  # TODO
                                      cluster_max_size=round(len(state.dataset.artifact_df) * cluster_reduction_factor))

        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()
        state.update_total_costs_from_state(clustering_pipeline.state)

        state.cluster_map = clustering_pipeline.state.final_cluster_map
