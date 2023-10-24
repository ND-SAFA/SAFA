from typing import Any, Iterable, List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from tgen.data.clustering.supported_clustering_method import SupportedClusteringMethod
from tgen.embeddings.embeddings_manager import EmbeddingType, EmbeddingsManager


class Cluster:
    """
    Manages a cluster in a dataset.
    """

    def __init__(self, embeddings_manager: EmbeddingsManager):
        """
        Constructs empty cluster referencing embeddings in manager.
        :param embeddings_manager: The container for all embeddings relating to cluster.
        """
        self.embeddings_manager = embeddings_manager
        self.artifact_ids = []
        self.artifact_id_set = set()
        self.votes = 1
        self.avg_similarity = None
        self.centroid = None

    @staticmethod
    def calculate_centroid(cluster: List[str], embedding_manager: EmbeddingsManager):
        """
        Calculates the embedding pointing at the center of the cluster.
        :param cluster: The artifacts whose embeddings are used to calculate the centroid.
        :param embedding_manager: Contains the artifacts embeddings.
        :return: Embedding pointing at center of cluster.
        """
        if len(cluster) == 0:
            raise Exception("Cannot calculate center of empty cluster.")
        embeddings = [embedding_manager.get_embedding(a_id) for a_id in cluster]
        centroid = np.sum(embeddings, axis=0) / len(cluster)
        return centroid

    @staticmethod
    def get_cluster_id(method: SupportedClusteringMethod, index: int):
        """
        Creates generic cluster id.
        :param method: The method used to generate the cluster.
        :param index: The index the cluster is stored in the cluster map.
        :return: The cluster id.
        """
        return f"{method.name}{index}"

    @staticmethod
    def calculate_average_similarity(cluster: List[str], centroid: EmbeddingType, embedding_manager: EmbeddingsManager):
        """
        Calculates the average similarity to the cluster centroid for all points in the cluster.
        :param cluster: The cluster containing the artifact ids.
        :param centroid: The embedding at the center of the cluster.
        :param embedding_manager: The manager able to retrieve embeddings for artifact ids.
        :return: Score representing the average similarity score to the cluster centroid.
        """
        embeddings = [embedding_manager.get_embedding(a_id) for a_id in cluster]
        similarities = cosine_similarity([centroid], embeddings)[0]
        avg_similarity = sum(similarities) / len(similarities)
        return avg_similarity

    @staticmethod
    def from_artifacts(artifact_ids: List[str], embeddings_manager: EmbeddingsManager) -> "Cluster":
        """
        Creates cluster containing given artifact ids.
        :param artifact_ids: The artifacts to include in the cluster.
        :param embeddings_manager: The embeddings manager used to update the stats of the cluster.
        :return: The cluster.
        """
        cluster = Cluster(embeddings_manager)
        cluster.add_artifacts(artifact_ids)
        return cluster

    def add_vote(self) -> None:
        """
        Adds vote to cluster.
        :return: None. Modified in place.
        """
        self.votes += 1

    def add_artifacts(self, artifact_ids: List[str]) -> None:
        """
        Adds multiple artifacts to cluster and updates its stats.
        :param artifact_ids: The artifact ids to add to the cluster.
        :return: None.
        """
        for artifact_id in artifact_ids:
            self._add_artifact(artifact_id)
        self.__update_stats()

    def add_artifact(self, artifact_id: str) -> None:
        """
        Adds an artifact to the cluster.
        :param artifact_id: ID of artifact to add to cluster.
        :return: None
        """
        self._add_artifact(artifact_id)
        self.__update_stats()

    def similarity_to(self, cluster: "Cluster") -> float:
        """
        Calculates the cosine similarity between the centroid of this cluster to the cluster given.
        :param cluster: The cluster to calculate the distance to.
        :return: The similarity to the other cluster.
        """
        return cosine_similarity([self.centroid], [cluster.centroid])[0][0]

    def _add_artifact(self, artifact_id: str) -> None:
        """
        Adds an artifact to the cluster.
        :param artifact_id: ID of artifact to add to cluster.
        :return: None
        """
        if artifact_id not in self.artifact_id_set:
            self.artifact_id_set.add(artifact_id)
            self.artifact_ids.append(artifact_id)

    def __update_stats(self) -> None:
        """
        Calculates all statistics for the cluster.
        :return: None, stats are set in place
        """
        self.centroid = Cluster.calculate_centroid(self.artifact_ids, self.embeddings_manager)
        self.avg_similarity = Cluster.calculate_average_similarity(self.artifact_ids, self.centroid, self.embeddings_manager)

    def __len__(self) -> int:
        """
        :return: Length of cluster is the number of the artifacts in cluster.
        """
        return len(self.artifact_id_set)

    def __iter__(self) -> Iterable[str]:
        """
        :return: Iterable goes through each artifact id.
        """
        for a in self.artifact_ids:
            yield a

    def __contains__(self, item: Any) -> bool:
        """
        Calculates whether item is an artifact ID in the cluster.
        :param item: The artifact ID.
        :return: True is artifact id in cluster, false otherwise.
        """
        return isinstance(item, str) and item in self.artifact_ids

    def __str__(self) -> str:
        """
        :return: Returns string version of the artifacts.
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        :return: Cluster is represented by the list of artifact ids it contains.
        """
        score = "" if self.avg_similarity is None else f"({round(self.avg_similarity, 2)})"
        cluster_repr = f"{self.artifact_ids.__str__()}{score}"
        return cluster_repr

    def __eq__(self, other: Any) -> bool:
        """
        Determines if other contains the same artifacts as this one.
        :param other: The other cluster to compare.
        :return: True if clusters have the same artifacts, false otherwise.
        """
        return isinstance(other, Cluster) and other.artifact_id_set.__eq__(self.artifact_id_set)

    def __hash__(self) -> List[Any]:
        """
        Makes this object hashable.
        # TODO: Replace this with the hash for a set.
        :return: The hash for each artifact id.
        """
        return hash("-".join(sorted(list(self.artifact_ids))))
