from typing import Any, Dict, List, Optional

import numpy as np
from tqdm import tqdm

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_condenser import ClusterCondenser
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.clustering_algorithm_manager import ClusteringAlgorithmManager
from tgen.common.constants.clustering_constants import MIN_PAIRWISE_AVG_PERCENTILE, MIN_PAIRWISE_SIMILARITY_FOR_CLUSTERING
from tgen.common.constants.logging_constants import TQDM_NCOLS
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep


class CreateClustersFromEmbeddings(AbstractPipelineStep):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Creates clusters from the embeddings.
        :param args: Args containing embedding map.
        :param state: Used to store final clusters.
        :return: None
        """
        batches = state.artifact_batches if state.artifact_batches else [args.get_artifact_ids()]
        global_clusters = {}
        for i, batch_ids in enumerate(batches):
            batch_cluster_map = CreateClustersFromEmbeddings.get_batch_clusters(args,
                                                                                state.embedding_manager,
                                                                                batch_artifact_ids=batch_ids)
            batch_cluster_map = CreateClustersFromEmbeddings.condense_clusters(args, state, batch_cluster_map, i)
            global_clusters.update(batch_cluster_map)
        state.final_cluster_map = global_clusters

    @staticmethod
    def condense_clusters(args: ClusteringArgs, state: ClusteringState, cluster_map: Dict, i: Any) -> ClusterMapType:
        """
        Condenses the clusters in the given map.
        :param args: Arguments of clustering pipeline.
        :param state: State of clustering pipeline.
        :param cluster_map: Map of method name to cluster to condense.
        :param i: The unique ID for this cluster.
        :return: The new cluster map.
        """
        unique_cluster_map = ClusterCondenser(state.embedding_manager, threshold=args.cluster_intersection_threshold)
        clusters = list(cluster_map.values())
        clusters = CreateClustersFromEmbeddings.cohesiveness_filter(args, clusters)
        unique_cluster_map.add_all(clusters)
        cluster_map = unique_cluster_map.get_clusters(args.cluster_min_votes)
        cluster_map = {f"{i}:{k}": v for k, v in cluster_map.items()}
        return cluster_map

    @staticmethod
    def cohesiveness_filter(args: ClusteringArgs, clusters: List[Cluster]):
        """
        Filters clusters by their cohesiveness relative to the average cohesiveness of all clusters.
        :param args: Clustering args determining if this step should be run.
        :param clusters: The clusters to filter.
        :return: List of filtered clusters.
        """
        filtered_clusters = CreateClustersFromEmbeddings._filter_by_size(clusters, args.cluster_min_size, args.cluster_max_size)
        min_pairwise_avg = CreateClustersFromEmbeddings._calculate_min_pairwise_avg_threshold(filtered_clusters)
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
        unique_clusters = set(clusters)
        cluster_scores = [cluster.avg_pairwise_sim for cluster in unique_clusters if cluster.avg_pairwise_sim is not None]
        if not cluster_scores:
            return None
        percentile_score = np.quantile(cluster_scores, MIN_PAIRWISE_AVG_PERCENTILE)
        final_score = min(percentile_score, MIN_PAIRWISE_SIMILARITY_FOR_CLUSTERING)
        return final_score

    @staticmethod
    def get_batch_clusters(args: ClusteringArgs, embeddings_manager: EmbeddingsManager,
                           batch_artifact_ids: List[str]) -> ClusterMapType:
        """
        Creates the clusters for a subset of artifacts.
        :param args: The clustering arguments / configuration.
        :param embeddings_manager: Contains the artifact embeddings to cluster.
        :param batch_artifact_ids: The artifacts ids to cluster.
        :return: Map of clustering method name to clusters produced by that method.
        """
        if isinstance(batch_artifact_ids, list) and len(batch_artifact_ids) == 0:
            return {}
        if len(batch_artifact_ids) < args.cluster_max_size:
            return {"singleton": Cluster.from_artifacts(batch_artifact_ids, embeddings_manager)}

        global_clusters: ClusterMapType = {}
        for clustering_method in tqdm(args.cluster_methods, desc="Running Clustering Algorithms...", ncols=TQDM_NCOLS):
            cluster_manager = ClusteringAlgorithmManager(clustering_method)
            clusters = cluster_manager.cluster(embeddings_manager, reduction_factor=args.cluster_reduction_factor,
                                               min_cluster_size=args.cluster_min_size, max_cluster_size=args.cluster_max_size,
                                               subset_ids=batch_artifact_ids,
                                               **args.clustering_method_args)
            clustering_method_name = cluster_manager.get_method_name()
            clusters = {f"{clustering_method_name}{k}": v for k, v in clusters.items()}
            global_clusters.update(clusters)
        return global_clusters
