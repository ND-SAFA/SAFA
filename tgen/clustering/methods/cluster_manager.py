from typing import Dict, List

from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.methods.supported_cluster_methods import SupportedClusterMethods
from tgen.embeddings.embeddings_manager import EmbeddingType

REQUIRED_CLUSTER_ESTIMATION = [SupportedClusterMethods.KMEANS, SupportedClusterMethods.AGGLOMERATIVE]


class ClusterManager:

    def __init__(self, method: SupportedClusterMethods):
        """
        Constructs clustering method for the given algorithm.
        :param method:
        """
        self.method = method

    def cluster(self, embedding_map: Dict[str, EmbeddingType], reduction_factor: float, **kwargs) -> ClusterMapType:
        """
        Clusters embeddings in map and creates sets of links.
        :param embedding_map: Map of artifact ID to embedding.
        :param reduction_factor: The factor by which the embeddings are reduced into clusters
        (e.g. 0.25 => # clusters = (embeddings / 4))
        :param kwargs: Clustering method arguments.
        :return: Map of cluster ID to artifact ids in cluster.
        """
        artifact_ids = list(embedding_map.keys())
        embeddings = [embedding_map[artifact_id] for artifact_id in artifact_ids]
        n_clusters = round(len(embeddings) * reduction_factor)

        local_kwargs = {} if self.method not in REQUIRED_CLUSTER_ESTIMATION else {"n_clusters": n_clusters}

        clustering_algo = self.method.value(**local_kwargs, **kwargs)
        clustering_algo.fit(embeddings)
        embedding_labels = clustering_algo.labels_
        clusters = self.create_clusters_from_labels(artifact_ids, embedding_labels)
        return clusters

    @staticmethod
    def create_clusters_from_labels(artifact_ids: List[str], cluster_labels: List[int]) -> ClusterMapType:
        """
        Creates cluster by linking cluster labels associated to each artifact.
        :param artifact_ids: The artifacts to cluster.
        :param cluster_labels: The cluster ID associated with each artifact.
        :return: Map of cluster to their corresponding artifacts.
        """
        clusters = {}
        for cluster_label, artifact_id in zip(cluster_labels, artifact_ids):
            if cluster_label not in clusters:
                clusters[cluster_label] = []
            clusters[cluster_label].append(artifact_id)
        return clusters

    def get_id(self) -> str:
        """
        :return: Returns string identifier for the method.
        """
        return self.method.name
