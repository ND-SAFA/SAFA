from dataclasses import dataclass, field
from typing import Dict, List

from tgen.clustering.methods.supported_clustering_methods import SupportedClusteringMethods
from tgen.common.constants import environment_constants
from tgen.common.constants.clustering_constants import DEFAULT_ADD_CLUSTERS_TO_DATASET, DEFAULT_CLUSTERING_METHODS, \
    DEFAULT_CLUSTER_MIN_VOTES, DEFAULT_CLUSTER_SIMILARITY_THRESHOLD, \
    DEFAULT_MIN_ORPHAN_SIMILARITY, DEFAULT_REDUCTION_FACTOR
from tgen.common.constants.ranking_constants import DEFAULT_EMBEDDING_MODEL, DEFAULT_SEARCH_EMBEDDING_MODEL
from tgen.pipeline.pipeline_args import PipelineArgs


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
    cluster_methods: List[SupportedClusteringMethods] = field(default_factory=lambda: DEFAULT_CLUSTERING_METHODS)
    clustering_method_args: Dict = field(default_factory=dict)
    embedding_model: str = None
    artifact_types: List[str] = None
    cluster_intersection_threshold: float = DEFAULT_CLUSTER_SIMILARITY_THRESHOLD  # 80% or more of intersection equals same cluster
    cluster_reduction_factor: float = DEFAULT_REDUCTION_FACTOR
    create_dataset: bool = DEFAULT_ADD_CLUSTERS_TO_DATASET
    cluster_min_votes: int = DEFAULT_CLUSTER_MIN_VOTES
    min_orphan_similarity: float = DEFAULT_MIN_ORPHAN_SIMILARITY

    def __post_init__(self) -> None:
        """
        Creates dataset if creator is defined, sets optional artifact types.
        :return: None
        """
        super().__post_init__()
        if self.embedding_model is None:
            self.embedding_model = DEFAULT_SEARCH_EMBEDDING_MODEL if environment_constants.IS_TEST else DEFAULT_EMBEDDING_MODEL
        if self.artifact_types is None:
            self.artifact_types = self.dataset.artifact_df.get_artifact_types()

        self.cluster_methods = [SupportedClusteringMethods[c] if isinstance(c, str) else c for c in self.cluster_methods]
