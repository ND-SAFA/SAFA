from gen_common.clustering.base.cluster_type import ClusterMapType
from gen_common.clustering.base.clustering_args import ClusteringArgs
from gen_common.clustering.clustering_pipeline import ClusteringPipeline
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.pipeline.state import State
from gen_common.pipeline.util import nested_pipeline
from gen_common.traceability.ranking.common.ranking_args import RankingArgs
from gen_common.traceability.ranking.common.ranking_state import RankingState
from gen_common.traceability.ranking.sorters.cluster_children_sorter import ClusterChildrenSorter
from gen_common.util.file_util import FileUtil
from gen_common.util.ranking_util import RankingUtil

USE_HGEN_TO_CLUSTER = False  # Will move this in the future when done experimenting


class ClusterAndSortArtifactsStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Sorts the children for each parent using clustering.
        :param args: The ranking arguments to the pipeline.
        :param state: The state of the current pipeline.
        :return: None
        """
        final_clusters = self.run_clustering(args, state)

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
