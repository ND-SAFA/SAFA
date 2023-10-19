from typing import Dict

from tgen.clustering.clustering_args import ClusterType
from tgen.state.state import State
from tgen.tracing.ranking.sorters.embedding_sorter import EmbeddingType


class ClusteringState(State):
    """
    The state of a clustering pipeline.
    :param embedding_map: Map of artifact ID to its embedding.
    :param clusters: Map of cluster ID to its artifacts.
    """
    embedding_map: Dict[str, EmbeddingType]
    clusters: ClusterType
