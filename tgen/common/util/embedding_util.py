from typing import List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from tgen.embeddings.embeddings_manager import EmbeddingType


class EmbeddingUtil:
    @classmethod
    def calculate_similarities_to_clusters(cls, embedding: EmbeddingType, clusters: List["Cluster"]) -> List[float]:
        """
        Calculates the similarities from the starting embeddings to the centroids of the clusters.
        :param embedding: The embeddings serving as the starting point.
        :param clusters: The clusters whose similarity to is calculated.
        :return: List of similarity scores to the clusters.
        """
        centroids = [c.centroid for c in clusters]
        cluster_similarities = cls.calculate_similarities([embedding], centroids)[0]
        return cluster_similarities

    @classmethod
    def calculate_similarity(cls, source_embedding: EmbeddingType, target_embedding: EmbeddingType) -> float:
        """
        Calculates similarity score between two embeddings.
        :param source_embedding: The first embedding.
        :param target_embedding: The second embedding.
        :return: The similarity score.
        """
        return cls.calculate_similarities([source_embedding], [target_embedding])[0][0]

    @staticmethod
    def calculate_similarities(source_embeddings: List[EmbeddingType], target_embeddings: List[EmbeddingType]) -> List[List[float]]:
        """
        Calculates the similarities between source and target embeddings.
        :param source_embeddings: Rows of similarity matrix.
        :param target_embeddings: Columns of similarity matrix.
        :return: Similarity matrix.
        """
        source_matrix = np.asarray(source_embeddings)
        target_matrix = np.asarray(target_embeddings)
        cluster_similarities = cosine_similarity(source_matrix, target_matrix)
        return cluster_similarities
