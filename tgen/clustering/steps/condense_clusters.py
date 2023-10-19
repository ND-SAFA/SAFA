from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.base.unique_cluster_map import UniqueClusterMap
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class CondenseClusters(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Condenses clusters into a unique set of clusters.
        :param args: The arguments to the clustering pipeline.
        :param state: Current state of the clustering pipeline.
        :return: None
        """
        cluster_map = state.multi_method_cluster_map

        clusters = list(cluster_map.values())
        clusters = list(sorted(clusters, key=lambda v: len(v), reverse=False))
        unique_cluster_map = UniqueClusterMap(threshold=args.cluster_intersection_threshold)
        unique_cluster_map.add_all(clusters)

        state.final_cluster_map = unique_cluster_map.get_clusters()
