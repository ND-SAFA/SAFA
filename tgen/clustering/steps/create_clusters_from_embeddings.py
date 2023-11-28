from typing import Any, Dict, List

from tqdm import tqdm

from tgen.clustering.base.cluster_condenser import ClusterCondenser
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.clustering_algorithm_manager import ClusteringAlgorithmManager
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
        unique_cluster_map = ClusterCondenser(state.embedding_manager,
                                              threshold=args.cluster_intersection_threshold,
                                              min_cluster_size=args.cluster_min_size,
                                              max_cluster_size=args.cluster_max_size,
                                              filter_cohesiveness=args.filter_by_cohesiveness)
        clusters = list(cluster_map.values())
        unique_cluster_map.add_all(clusters)
        cluster_map = unique_cluster_map.get_clusters(args.cluster_min_votes)
        cluster_map = {f"{i}:{k}": v for k, v in cluster_map.items()}
        return cluster_map

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
