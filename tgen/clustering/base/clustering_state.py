from dataclasses import dataclass

from tgen.clustering.base.cluster_type import ClusterMapType, MethodClusterMapType
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.state.state import State


@dataclass
class ClusteringState(State):
    """
    The state of a clustering pipeline.
    :param embedding_manager: Map of artifact ID to its embedding.
    :param multi_method_cluster_map: Map of cluster ID to its artifacts.
    :TODO: param docs.
    """
    embedding_manager: EmbeddingsManager = None
    multi_method_cluster_map: MethodClusterMapType = None
    final_cluster_map: ClusterMapType = None
    cluster_artifact_dataset: PromptDataset = None
    cluster_dataset: PromptDataset = None
