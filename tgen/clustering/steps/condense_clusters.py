from tgen.clustering.base.cluster_selector import ClusterSelector
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.common.constants.clustering_constants import MIN_AVG_SIMILARITY_FOR_CLUSTERING
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class CondenseClusters(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Condenses clusters into a unique set of clusters.
        :param args: The arguments to the clustering pipeline.
        :param state: Current state of the clustering pipeline.
        :return: None
        """
        global_cluster_map = state.multi_method_cluster_map
        unique_cluster_map = ClusterSelector(state.embedding_manager, threshold=args.cluster_intersection_threshold)

        clusters = []
        for cluster_method in args.cluster_methods:
            cluster_map = global_cluster_map[cluster_method.name]
            clusters.extend(list(cluster_map.values()))
        clusters = list(filter(lambda c: c.avg_similarity >= MIN_AVG_SIMILARITY_FOR_CLUSTERING, clusters))
        clusters = list(sorted(clusters, key=lambda v: (len(v), v.avg_similarity), reverse=True))
        unique_cluster_map.add_all(clusters)

        final_clusters = unique_cluster_map.get_clusters(args.cluster_min_votes)
        state.final_cluster_map = final_clusters
