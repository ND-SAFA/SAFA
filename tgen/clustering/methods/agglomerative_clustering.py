from typing import List

from sklearn.cluster import AgglomerativeClustering

from tgen.clustering.methods.icluster_method import IClusterMethod
from tgen.embeddings.embeddings_manager import EmbeddingType

DEFAULT_REDUCTION_FACTOR = 0.25  # Expected reduction in artifacts
DEFAULT_RANDOM_STATE = 0


class AgglomerativeClusteringMethod(IClusterMethod):

    def _cluster(self, embeddings: List[EmbeddingType], reduction_factor: float = DEFAULT_REDUCTION_FACTOR,
                 random_state: int = DEFAULT_RANDOM_STATE, **kwargs) -> List[int]:
        """
        Performs K-Means clustering on the embeddings.
        :param embeddings: The embeddings to cluster.
        :param reduction_factor: The reduction factor used to calculate how many clusters to produce.
        :param random_state: The random state of the KMeans algo.
        :param n_init: The number of times to re-initialize kmeans.
        :return: The labels associated with each embedding.
        """
        agglomerative_clustering = AgglomerativeClustering()
        agglomerative_clustering.fit(embeddings)
        return agglomerative_clustering.labels_

    def get_id(self) -> str:
        """
        :return: Identifier for method.
        """
        return "AGG"
