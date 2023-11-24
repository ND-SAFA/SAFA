from typing import List, Optional

import numpy as np

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_condenser import ClusterCondenser
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.common.constants.clustering_constants import MIN_PAIRWISE_AVG_PERCENTILE, MIN_PAIRWISE_SIMILARITY_FOR_CLUSTERING
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class CondenseClusters(AbstractPipelineStep[ClusteringArgs, ClusteringState]):

    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Condenses clusters into a unique set of clusters.
        :param args: The arguments to the clustering pipeline.
        :param state: Current state of the clustering pipeline.
        :return: None
        """
        global_batch_cluster_map: List[ClusterMapType] = state.batched_cluster_maps

        global_clusters = {}
        for i, batch_cluster_map in enumerate(global_batch_cluster_map):
            unique_cluster_map = ClusterCondenser(state.embedding_manager, threshold=args.cluster_intersection_threshold)
            clusters = list(batch_cluster_map.values())

            clusters = self.cohesiveness_filter(args, clusters)
            unique_cluster_map.add_all(clusters)

            batch_cluster_map = unique_cluster_map.get_clusters(args.cluster_min_votes)
            batch_cluster_map = {f"{i}:{k}": v for k, v in batch_cluster_map.items()}
            global_clusters.update(batch_cluster_map)

        final_clusters = global_clusters
        state.final_cluster_map = final_clusters

    def cohesiveness_filter(self, args: ClusteringArgs, clusters: List[Cluster]):
        """
        Filters clusters by their cohesiveness relative to the average cohesiveness of all clusters.
        :param args: Clustering args determining if this step should be run.
        :param clusters: The clusters to filter.
        :return: List of filtered clusters.
        """
        filtered_clusters = self._filter_by_size(clusters, args.cluster_min_size, args.cluster_max_size)
        min_pairwise_avg = self._calculate_min_pairwise_avg_threshold(filtered_clusters)
        if min_pairwise_avg is not None:
            if args.filter_by_cohesiveness:
                clusters = list(filter(lambda c: c.avg_pairwise_sim >= min_pairwise_avg, filtered_clusters))
            clusters = list(sorted(clusters, key=lambda v: v.avg_pairwise_sim if v.avg_pairwise_sim else 0, reverse=True))
        return clusters

    @staticmethod
    def _filter_by_size(clusters: List[Cluster], min_size: int, max_size: int):
        """
        Filters list of clusters by min and max size. If there are no resulting clusters then original list if returned.
        :param clusters: The clusters to filter.
        :param min_size: The minimum size of a cluster.
        :param max_size: The maximum size of a cluster.
        :return: The filtered clusters within the size bounds.
        """
        filter_clusters = [c for c in clusters if min_size <= len(c) <= max_size]
        clusters = filter_clusters if filter_clusters else clusters
        return clusters

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
