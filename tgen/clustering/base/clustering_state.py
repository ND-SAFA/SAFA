from dataclasses import dataclass
from typing import List

from tgen.clustering.base.cluster_type import ClusterIdType, ClusterMapType
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.pipeline.state import State


@dataclass
class ClusteringState(State):
    """
    The state of a clustering pipeline.
    :param embedding_manager: Map of artifact ID to its embedding.
    :param batched_cluster_maps: Map of cluster ID to its artifacts.
    :param cluster_artifact_dataset: The dataset containing the source artifacts, clusters, links between them.
    :param cluster2artifacts: Map of seeds to their cluster of source artifact ids.
    :param artifact_batches: The batches of artifacts to cluster. When seeds are provided the batches represent each seed.
    :param final_cluster_map: Map of cluster_id to Cluster containing artifacts.
    """
    embedding_manager: EmbeddingsManager = None
    batched_cluster_maps: List[ClusterMapType] = None
    cluster_artifact_dataset: PromptDataset = None
    cluster_dataset: PromptDataset = None
    cluster2artifacts: ClusterIdType = None
    artifact_batches: List[List[str]] = None
    final_cluster_map: ClusterMapType = None
