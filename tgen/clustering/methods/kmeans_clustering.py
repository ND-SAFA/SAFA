from typing import List

from sklearn.cluster import KMeans

from tgen.clustering.methods.icluster_method import IClusterMethod
from tgen.embeddings.embeddings_manager import EmbeddingType

DEFAULT_REDUCTION_FACTOR = 0.25  # Expected reduction in artifacts
DEFAULT_RANDOM_STATE = 0


class KMeansClustering(IClusterMethod):
    def _cluster(self, embeddings: List[EmbeddingType], n_clusters: int, random_state: int = DEFAULT_RANDOM_STATE, **kwargs) -> List[
        int]:
        """
        Performs K-Means clustering on the embeddings.
        :param embeddings: The embeddings to cluster.
        :param reduction_factor: The reduction factor used to calculate how many clusters to produce.
        :param random_state: The random state of the KMeans algo.
        :param n_init: The number of times to re-initialize kmeans.
        :return: The labels associated with each embedding.
        """
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, **kwargs)
        kmeans.fit(embeddings)
        return kmeans.labels_

    def get_id(self) -> str:
        """
        :return: Identifier for method.
        """
        return "KMEANS"
