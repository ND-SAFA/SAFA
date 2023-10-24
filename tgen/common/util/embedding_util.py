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

    @staticmethod
    def calculate_similarities(source_embeddings: List[EmbeddingType], target_embeddings: List[EmbeddingType]) -> List[List[float]]:
        """
        Calculates the similarities between source and target embeddings.
        :param source_embeddings: Rows of similarity matrix.
        :param target_embeddings: Columns of similarity matrix.
        :return: Similarity matrix.
        """
        source_matrix = np.matrix(source_embeddings)
        target_matrix = np.matrix(target_embeddings)
        cluster_similarities = cosine_similarity(source_matrix, target_matrix)
        return cluster_similarities
