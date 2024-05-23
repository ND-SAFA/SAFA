from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.util.file_util import FileUtil
from tgen.common.util.pipeline_util import nested_pipeline
from tgen.data.keys.structure_keys import TraceKeys, ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hierarchy_generator import HierarchyGenerator
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.pipeline.state import State
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.sorters.cluster_children_sorter import ClusterChildrenSorter

USE_HGEN_TO_CLUSTER = False  # Will move this in the future when done experimenting


class ClusterAndSortArtifactsStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Sorts the children for each parent using clustering.
        :param args: The ranking arguments to the pipeline.
        :param state: The state of the current pipeline.
        :return: None
        """
        clustering_method = self.run_clustering_with_hgen if USE_HGEN_TO_CLUSTER else self.run_clustering
        final_clusters = clustering_method(args, state)

        state.artifact_map = args.dataset.artifact_df.to_map()
        sorter = ClusterChildrenSorter
        parent2rankings = sorter.sort(args.parent_ids, args.children_ids,
                                      embedding_manager=args.embeddings_manager,
                                      final_clusters=final_clusters,
                                      return_scores=True)
        state.sorted_parent2children = {p: [RankingUtil.create_entry(p, rankings[0][i], score=rankings[1][i])
                                            for i in range(len(rankings[0]))]
                                        for p, rankings in parent2rankings.items()}

    @staticmethod
    @nested_pipeline(RankingState)
    def run_clustering(args: RankingArgs, state: RankingState) -> ClusterMapType:
        """
         Runs the HGen pipeline to create clusters for sorting.
        :param args: The ranking arguments to the pipeline.
        :param state: The current Ranking state.
        :return: The map of final clusters
        """
        clustering_args = ClusteringArgs(dataset=args.dataset, save_initial_clusters=True,
                                         artifact_types=[args.child_type()],
                                         export_dir=FileUtil.safely_join_paths(args.export_dir, "clustering"))
        clustering_pipeline = ClusteringPipeline(clustering_args)
        clustering_pipeline.run()
        clustering_state = clustering_pipeline.state
        ClusterAndSortArtifactsStep._save_embeddings_manager(clustering_state, ranking_args=args, ranking_state=state)

        return clustering_state.final_cluster_map

    @staticmethod
    @nested_pipeline(RankingState)
    def run_clustering_with_hgen(args: RankingArgs, state: RankingState) -> ClusterMapType:
        """
         Runs the HGen pipeline to create clusters for sorting.
        :param args: The ranking arguments to the pipeline.
        :param state: The current Ranking state.
        :return: The map of final clusters
        """
        parent_type, child_type = args.types_to_trace
        hgen_args = HGenArgs(dataset=PromptDataset(artifact_df=args.dataset.artifact_df.filter_by_index(args.children_ids)),
                             source_layer_ids=child_type, target_type=parent_type,
                             export_dir=FileUtil.safely_join_paths(args.export_dir, "hgen"),
                             generate_explanations=False
                             )
        hgen_pipeline = HierarchyGenerator(hgen_args)
        hgen_pipeline.run()
        hgen_state = hgen_pipeline.state
        ClusterAndSortArtifactsStep._save_embeddings_manager(hgen_state, ranking_args=args, ranking_state=state)

        generated_artifacts = hgen_state.final_dataset.artifact_df.get_artifacts_by_type(parent_type)
        traces = hgen_state.final_dataset.trace_dataset.trace_df.get_links(true_only=True)
        parent2traces = RankingUtil.group_trace_predictions(traces, TraceKeys.parent_label())
        clusters = {artifact[ArtifactKeys.ID]:
                        [trace[TraceKeys.child_label()] for trace in parent2traces.get(artifact[ArtifactKeys.ID], [])]
                    for i, artifact in generated_artifacts.itertuples()}
        final_clusters = {p_id: Cluster.from_artifacts(a_ids,
                                                       args.embeddings_manager)
                          for p_id, a_ids in clusters.items() if len(a_ids) > 0}
        return final_clusters

    @staticmethod
    def _save_embeddings_manager(external_pipeline_state: State, ranking_state: RankingState, ranking_args: RankingArgs) -> None:
        """
        Saves the embedding manager from an external pipeline to the ranking state.
        :param external_pipeline_state: The state of the external pipeline with an embeddings manager.
        :param ranking_state: The current Ranking state.
        :param ranking_args: The arguments to the Ranking pipeline.
        :return: None
        """
        parent_artifact_map = ranking_args.dataset.artifact_df.get_artifacts_by_type(ranking_args.parent_type()).to_map()
        if hasattr(external_pipeline_state, "embedding_manager"):
            embedding_manager = external_pipeline_state.embedding_manager
            embedding_manager.update_or_add_contents(parent_artifact_map)
            embedding_manager.create_embedding_map()
            ranking_args.embeddings_manager = embedding_manager
