from typing import List

from sklearn.cluster import AgglomerativeClustering

from tgen.clustering.methods.icluster_method import IClusterMethod
from tgen.embeddings.embeddings_manager import EmbeddingType


class AgglomerativeClusteringMethod(IClusterMethod):
    """
    Docs: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html#sklearn.cluster.AgglomerativeClustering
    """

    def _cluster(self, embeddings: List[EmbeddingType], n_clusters: int, **kwargs) -> List[int]:
        """
        Performs K-Means clustering on the embeddings.
        :param embeddings: The embeddings to cluster.
        :param n_clusters: The expected number of clusters.
        :return: The labels associated with each embedding.
        """
        agglomerative_clustering = AgglomerativeClustering(n_clusters=n_clusters)
        agglomerative_clustering.fit(embeddings)
        return agglomerative_clustering.labels_

    def get_id(self) -> str:
        """
        :return: Identifier for method.
        """
        return "AGGLOMERATIVE"
