from typing import Dict, List

from sklearn.cluster import KMeans

from tgen.clustering.methods.icluster_method import IClusterMethod
from tgen.tracing.ranking.sorters.embedding_sorter import EmbeddingType

DEFAULT_REDUCTION_FACTOR = 0.25  # Expected reduction in artifacts
DEFAULT_RANDOM_STATE = 0
DEFAULT_N_INIT = "auto"


class KMeansClustering(IClusterMethod):
    def _cluster(self, embeddings: List[EmbeddingType], args: Dict) -> List[int]:
        reduction_factor = args.get("reduction_factor", DEFAULT_REDUCTION_FACTOR)
        random_state = args.get("random_state", DEFAULT_RANDOM_STATE)
        n_init = args.get("n_init", DEFAULT_N_INIT)

        n_clusters = round(len(embeddings) * reduction_factor)
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=n_init)
        kmeans.fit(embeddings)
        return kmeans.labels_
