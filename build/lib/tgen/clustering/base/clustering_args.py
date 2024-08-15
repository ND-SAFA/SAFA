from dataclasses import dataclass, field
from typing import Dict, List

from common_resources.tools.constants import environment_constants
from common_resources.tools.constants.environment_constants import DEFAULT_EMBEDDING_MODEL
from common_resources.tools.constants.model_constants import DEFAULT_TEST_EMBEDDING_MODEL
from common_resources.tools.state_management.args import Args
from common_resources.traceability.relationship_manager.embeddings_manager import EmbeddingsManager

from tgen.clustering.methods.supported_clustering_methods import SupportedClusteringMethods
from tgen.clustering.methods.supported_seed_clustering_methods import SupportedSeedClusteringMethods
from tgen.common.constants.clustering_constants import CLUSTER_ARTIFACT_TYPE, DEFAULT_ADD_CLUSTERS_TO_DATASET, \
    DEFAULT_CLUSTERING_METHODS, \
    DEFAULT_CLUSTER_MIN_VOTES, DEFAULT_CLUSTER_SIMILARITY_THRESHOLD, \
    DEFAULT_FILTER_BY_COHESIVENESS, DEFAULT_MAX_CLUSTER_SIZE, DEFAULT_MIN_CLUSTER_SIZE, DEFAULT_MIN_ORPHAN_SIMILARITY, \
    DEFAULT_SEED_CLUSTERING_METHOD, DEFAULT_SORT_METRIC


@dataclass
class ClusteringArgs(Args):
    """
    :param: clustering_methods: The methods used to create different clusters from the embeddings.
    :param clustering_method_args: Keyword arguments to pass to each clustering method.
    :param embedding_model: The name of the model to use to create the embeddings.
    :param artifact_types: List of artifact types to cluster.
    :param cluster_intersection_threshold: Percentage of intersection between sets to consider them the same.
    :param dataset_creator: The creator used to get the dataset.
    :param dataset: The dataset to cluster.
    :param cluster_seeds: The centroids for clusters in a project.
    :param cluster_artifact_type: The artifact type whose artifacts are used as centroids.
    """
    cluster_methods: List[SupportedClusteringMethods] = field(default_factory=lambda: DEFAULT_CLUSTERING_METHODS)
    clustering_method_args: Dict = field(default_factory=dict)
    embedding_model: str = None
    embedding_manager: EmbeddingsManager = None
    artifact_types: List[str] = None
    cluster_max_size: int = DEFAULT_MAX_CLUSTER_SIZE
    cluster_min_size: int = DEFAULT_MIN_CLUSTER_SIZE
    cluster_intersection_threshold: float = DEFAULT_CLUSTER_SIMILARITY_THRESHOLD  # 80% or more of intersection equals same cluster
    create_dataset: bool = DEFAULT_ADD_CLUSTERS_TO_DATASET
    cluster_min_votes: int = DEFAULT_CLUSTER_MIN_VOTES
    add_orphans_to_homes: bool = True
    min_orphan_similarity: float = DEFAULT_MIN_ORPHAN_SIMILARITY
    cluster_seeds: List[str] = None
    cluster_artifact_type: str = CLUSTER_ARTIFACT_TYPE
    filter_by_cohesiveness: bool = DEFAULT_FILTER_BY_COHESIVENESS
    add_orphans_to_best_home: bool = False
    allow_singleton_clusters: bool = True
    allow_duplicates_between_clusters: bool = True
    subset_ids: List[str] = None
    seed_clustering_method: SupportedSeedClusteringMethods = DEFAULT_SEED_CLUSTERING_METHOD
    save_initial_clusters: bool = False
    metric_to_order_clusters: str = DEFAULT_SORT_METRIC
    use_ids_as_content: bool = False

    def __post_init__(self) -> None:
        """
        Creates dataset if creator is defined, sets optional artifact types.
        :return: None
        """
        super().__post_init__()
        if self.embedding_model is None:
            self.embedding_model = DEFAULT_TEST_EMBEDDING_MODEL if environment_constants.IS_TEST else DEFAULT_EMBEDDING_MODEL
        if self.artifact_types is None:
            self.artifact_types = self.dataset.artifact_df.get_artifact_types()

        self.cluster_methods = [SupportedClusteringMethods[c] if isinstance(c, str) else c for c in self.cluster_methods]

    def get_artifact_ids(self) -> List[str]:
        """
        :return: Returns the artifact ids in scope for this pipeline.
        """
        if self.artifact_types:
            artifact_df = self.dataset.artifact_df.get_artifacts_by_type(self.artifact_types)
        else:
            artifact_df = self.dataset.artifact_df
        artifact_ids = list(artifact_df.index)
        return self.subset_ids if self.subset_ids else artifact_ids
