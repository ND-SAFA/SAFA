from typing import Any, Iterable, List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from tgen.embeddings.embeddings_manager import EmbeddingType, EmbeddingsManager


class Cluster:
    """
    Manages a cluster in a dataset.
    """

    def __init__(self):
        """
        Constructs empty cluster.
        """
        self.artifact_ids = []
        self.artifact_id_set = set()
        self.votes = 1
        self.avg_similarity = None
        self.centroid = None

    def add_vote(self) -> None:
        """
        Adds vote to cluster.
        :return: None
        """
        self.votes += 1

    def add_artifact(self, artifact_id: str) -> None:
        """
        Adds an artifact to the cluster.
        :param artifact_id: ID of artifact to add to cluster.
        :return: None
        """
        self.artifact_ids.append(artifact_id)
        self.artifact_id_set.add(artifact_id)

    def calculate_stats(self, embedding_manager: EmbeddingsManager) -> None:
        """
        Calculates all statistics for the cluster.
        :param embedding_manager: Manager containing embeddings for artifacts in cluster.
        :return: None, stats are set in place
        """
        self.centroid = self.calculate_centroid(self.artifact_ids, embedding_manager)
        self.avg_similarity = self.calculate_average_similarity(self.artifact_ids, self.centroid, embedding_manager)

    @staticmethod
    def calculate_average_similarity(cluster: List[str], centroid: EmbeddingType, embedding_manager: EmbeddingsManager):
        """
        Calculates the average similarity to the cluster centroid for all points in the cluster.
        :param cluster: The cluster containing the artifact ids.
        :param centroid: The embedding at the center of the cluster.
        :param embedding_manager: The manager able to retrieve embeddings for artifact ids.
        :return: Score representing the average similarity score to the cluster centroid.
        """
        embeddings = [embedding_manager.get_embedding(c) for c in cluster]
        similarities = cosine_similarity([centroid], embeddings)[0]
        avg_similarity = sum(similarities) / len(similarities)
        return avg_similarity

    @staticmethod
    def calculate_centroid(cluster: List[str], embedding_manager: EmbeddingsManager):
        """
        Calculates the embedding pointing at the center of the cluster.
        :param cluster: The artifacts whose embeddings are used to calculate the centroid.
        :param embedding_manager: Contains the artifacts embeddings.
        :return: Embedding pointing at center of cluster.
        """
        embeddings = [embedding_manager.get_embedding(c) for c in cluster]
        centroid = np.sum(embeddings, axis=0) / len(cluster)
        return centroid

    def id(self) -> str:
        """
        :return: Returns ID for cluster representing artifact ids.
        """
        score = "" if self.avg_similarity is None else f"({round(self.avg_similarity, 2)})"
        return f"{self.artifact_ids.__str__()}{score}"

    def __len__(self) -> int:
        """
        :return: Length of cluster is the number of the artifacts in cluster.
        """
        return len(self.artifact_ids)

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
        return self.id()

    def __repr__(self) -> str:
        """
        :return: Cluster is represented by the list of artifact ids it contains.
        """
        return self.id()

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
        :return:
        """
        return self.artifact_id_set.__hash__()
