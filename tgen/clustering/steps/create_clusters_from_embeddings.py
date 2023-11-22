from typing import List

from tqdm import tqdm

from tgen.clustering.base.cluster_type import MethodClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.clustering_algorithm_manager import ClusteringAlgorithmManager
from tgen.common.constants.logging_constants import TQDM_NCOLS
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateClustersFromEmbeddings(AbstractPipelineStep):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Creates clusters from the embeddings.
        :param args: Args containing embedding map.
        :param state: Used to store final clusters.
        :return: None
        """
        global_batch_clusters: List[MethodClusterMapType] = []
        batches = state.artifact_batches if state.artifact_batches else [None]
        for subset_ids in batches:
            global_clusters = {} if len(subset_ids) == 0 else self.get_batch_clusters(args, state.embedding_manager, subset_ids)
            global_batch_clusters.append(global_clusters)
        state.multi_method_cluster_map = global_batch_clusters

    @staticmethod
    def get_batch_clusters(args: ClusteringArgs, embeddings_manager: EmbeddingsManager, batch_artifact_ids: List[str]):
        """
        Creates the clusters for a subset of artifacts.
        :param args: The clustering arguments / configuration.
        :param embeddings_manager: Contains the artifact embeddings to cluster.
        :param batch_artifact_ids: The artifacts ids to cluster.
        :return: Map of clustering method name to clusters produced by that method.
        """
        global_clusters = {}
        for clustering_method in tqdm(args.cluster_methods, desc="Running Clustering Algorithms...", ncols=TQDM_NCOLS):
            cluster_manager = ClusteringAlgorithmManager(clustering_method)
            clusters = cluster_manager.cluster(embeddings_manager, args.cluster_reduction_factor, subset_ids=batch_artifact_ids,
                                               **args.clustering_method_args)
            clustering_method_name = cluster_manager.get_method_name()
            clusters = {f"{clustering_method_name}{k}": v for k, v in clusters.items()}
            global_clusters[clustering_method.name] = clusters
        return global_clusters
