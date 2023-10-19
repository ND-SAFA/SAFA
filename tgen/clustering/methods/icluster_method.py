from abc import ABC, abstractmethod
from typing import Dict, List

from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.embeddings.embeddings_manager import EmbeddingType


class IClusterMethod(ABC):

    def cluster(self, embedding_map: Dict[str, EmbeddingType], **kwargs) -> ClusterMapType:
        """
        Clusters embeddings in map and creates sets of links.
        :param embedding_map: Map of artifact ID to embedding.
        :param kwargs: Clustering method arguments.
        :return: Map of cluster ID to artifact ids in cluster.
        """
        artifact_ids = list(embedding_map.keys())
        embeddings = [embedding_map[artifact_id] for artifact_id in artifact_ids]
        embedding_labels = self._cluster(embeddings, **kwargs)
        clusters = self.create_clusters_from_labels(artifact_ids, embedding_labels)
        return clusters

    @abstractmethod
    def _cluster(self, embeddings: List[EmbeddingType], **kwargs) -> List[int]:
        """
        Clusters embeddings in map and creates sets of links.
        :param embeddings: The embeddings to cluster.
        :param args: Clustering method arguments.
        :return: Cluster ID mapped to each embedding.
        """
        pass

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

    @abstractmethod
    def get_id(self) -> str:
        """
        :return: Returns string identifier for the method.
        """
        pass
