from dataclasses import dataclass
from typing import Dict, List

from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.pipeline.state import State
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager

from gen_common.clustering.base.cluster_type import ClusterIdType, ClusterMapType


@dataclass
class ClusteringState(State):
    """
    The state of a clustering pipeline.
    :param embedding_manager: Map of artifact ID to its embedding.
    :param cluster_artifact_dataset: The dataset containing only source artifacts.
    :param cluster_dataset: The dataset containing the source artifacts, clusters, links between them.
    :param artifact_batches: The batches of artifacts to cluster. When seeds are provided the batches represent each seed.
    :param seed2artifacts: Map of seeds to their cluster of source artifact ids.
    :param final_cluster_map: Map of cluster_id to Cluster containing artifacts after condensing.
    :param initial_cluster_map: Map of cluster_id to Cluster containing artifacts before condensing.
    """
    embedding_manager: EmbeddingsManager = None
    cluster_artifact_dataset: PromptDataset = None
    cluster_dataset: PromptDataset = None
    artifact_batches: List[List[str]] = None
    seed2artifacts: ClusterIdType = None
    cluster_id_2seeds: Dict = None
    initial_cluster_map: ClusterMapType = None
    final_cluster_map: ClusterMapType = None
