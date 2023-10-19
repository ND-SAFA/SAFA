from typing import List

from sklearn.cluster import KMeans

from tgen.clustering.methods.icluster_method import IClusterMethod
from tgen.tracing.ranking.sorters.embedding_sorter import EmbeddingType

DEFAULT_REDUCTION_FACTOR = 0.25  # Expected reduction in artifacts
DEFAULT_RANDOM_STATE = 0
DEFAULT_N_INIT = "auto"


class KMeansClustering(IClusterMethod):
    def _cluster(self, embeddings: List[EmbeddingType], reduction_factor: float = DEFAULT_REDUCTION_FACTOR,
                 random_state: int = DEFAULT_RANDOM_STATE, n_init: int = DEFAULT_N_INIT) -> List[int]:
        """
        Performs K-Means clustering on the embeddings.
        :param embeddings: The embeddings to cluster.
        :param reduction_factor: The reduction factor used to calculate how many clusters to produce.
        :param random_state: The random state of the KMeans algo.
        :param n_init: The number of times to re-initialize kmeans.
        :return: The labels associated with each embedding.
        """
        n_clusters = round(len(embeddings) * reduction_factor)
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=n_init)
        kmeans.fit(embeddings)
        return kmeans.labels_
