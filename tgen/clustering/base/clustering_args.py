from dataclasses import dataclass, field
from typing import Dict, List

from tgen.clustering.methods.supported_cluster_methods import SupportedClusterMethods
from tgen.common.constants.clustering_constants import DEFAULT_ADD_CLUSTERS_TO_DATASET, DEFAULT_CLUSTERING_METHODS, \
    DEFAULT_CLUSTER_MIN_VOTES, DEFAULT_CLUSTER_SIMILARITY_THRESHOLD, \
    DEFAULT_REDUCTION_FACTOR
from tgen.common.constants.ranking_constants import DEFAULT_EMBEDDING_MODEL
from tgen.state.pipeline.pipeline_args import PipelineArgs


@dataclass
class ClusteringArgs(PipelineArgs):
    """
    :param: clustering_methods: The methods used to create different clusters from the embeddings.
    :param clustering_method_args: Keyword arguments to pass to each clustering method.
    :param embedding_model: The name of the model to use to create the embeddings.
    :param artifact_types: List of artifact types to cluster.
    :param cluster_intersection_threshold: Percentage of intersection between sets to consider them the same.
    :param dataset_creator: The creator used to get the dataset.
    :param dataset: The dataset to cluster.

    """
    cluster_methods: List[SupportedClusterMethods] = field(default_factory=lambda: DEFAULT_CLUSTERING_METHODS)
    clustering_method_args: Dict = field(default_factory=dict)
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    artifact_types: List[str] = None
    cluster_intersection_threshold: float = DEFAULT_CLUSTER_SIMILARITY_THRESHOLD  # 80% or more of intersection equals same cluster
    cluster_reduction_factor: float = DEFAULT_REDUCTION_FACTOR
    add_to_dataset: bool = DEFAULT_ADD_CLUSTERS_TO_DATASET
    cluster_min_votes: int = DEFAULT_CLUSTER_MIN_VOTES

    def __post_init__(self) -> None:
        """
        Creates dataset if creator is defined, sets optional artifact types.
        :return: None
        """
        super().__post_init__()
        if self.artifact_types is None:
            self.artifact_types = self.dataset.artifact_df.get_artifact_types()

        self.cluster_methods = [SupportedClusterMethods[c] if isinstance(c, str) else c for c in self.cluster_methods]
