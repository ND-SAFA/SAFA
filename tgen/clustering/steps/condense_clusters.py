from typing import List, Optional

import numpy as np

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_condenser import ClusterCondenser
from tgen.clustering.base.cluster_type import MethodClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.common.constants.clustering_constants import MAX_CLUSTER_SIZE, MIN_CLUSTER_SIZE, MIN_PAIRWISE_AVG_PERCENTILE, \
    MIN_PAIRWISE_SIMILARITY_FOR_CLUSTERING
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class CondenseClusters(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Condenses clusters into a unique set of clusters.
        :param args: The arguments to the clustering pipeline.
        :param state: Current state of the clustering pipeline.
        :return: None
        """
        global_cluster_map: MethodClusterMapType = state.multi_method_cluster_map
        unique_cluster_map = ClusterCondenser(state.embedding_manager, threshold=args.cluster_intersection_threshold)

        clusters = []
        for cluster_method in args.cluster_methods:
            cluster_map = global_cluster_map[cluster_method.name]
            clusters.extend(list(cluster_map.values()))

        filter_clusters = [c for c in clusters if MIN_CLUSTER_SIZE <= len(c) <= MAX_CLUSTER_SIZE]
        clusters = filter_clusters if filter_clusters else clusters
        min_pairwise_avg = self._calculate_min_pairwise_avg_threshold(filter_clusters)
        if min_pairwise_avg is not None:
            clusters = list(filter(lambda c: c.avg_pairwise_sim >= min_pairwise_avg, filter_clusters))
            clusters = list(sorted(clusters, key=lambda v: v.avg_pairwise_sim, reverse=True))
        unique_cluster_map.add_all(clusters)

        final_clusters = unique_cluster_map.get_clusters(args.cluster_min_votes)
        state.final_cluster_map = final_clusters

    @staticmethod
    def _calculate_min_pairwise_avg_threshold(clusters: List[Cluster]) -> Optional[float]:
        """
        Calculates the minimum acceptable pairwise similarity for a cluster based on the minimum avg of the artifacts in all clusters
        :param clusters: List of the clusters to base the threshold on
        :return: The threshold for the minimum acceptable pairwise similarity
        """
        pairwise_avgs = [cluster.avg_pairwise_sim for cluster in clusters if cluster.avg_pairwise_sim is not None]
        if not pairwise_avgs:
            return None
        if max(pairwise_avgs) >= MIN_PAIRWISE_SIMILARITY_FOR_CLUSTERING:
            return MIN_PAIRWISE_SIMILARITY_FOR_CLUSTERING
        return np.percentile(pairwise_avgs, MIN_PAIRWISE_AVG_PERCENTILE)
