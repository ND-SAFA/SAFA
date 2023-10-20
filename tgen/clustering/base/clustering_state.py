from typing import Dict

from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.embeddings.embeddings_manager import EmbeddingType
from tgen.state.state import State


class ClusteringState(State):
    """
    The state of a clustering pipeline.
    :param embedding_map: Map of artifact ID to its embedding.
    :param multi_method_cluster_map: Map of cluster ID to its artifacts.
    """
    embedding_map: Dict[str, EmbeddingType]
    multi_method_cluster_map: Dict[str, ClusterMapType]
    final_cluster_map: ClusterMapType
