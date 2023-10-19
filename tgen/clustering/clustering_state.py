from tgen.clustering.clustering_args import ClusterType
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.state.state import State


class ClusteringState(State):
    """
    The state of a clustering pipeline.
    :param embedding_manager: Map of artifact ID to its embedding.
    :param clusters: Map of cluster ID to its artifacts.
    """
    embedding_manager: EmbeddingsManager
    clusters: ClusterType
