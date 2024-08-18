from gen_common.clustering.base.supported_cluster_sort_metrics import SupportedClusterSortMetrics
from gen_common.clustering.methods.supported_clustering_methods import SupportedClusteringMethods
from gen_common.clustering.methods.supported_seed_clustering_methods import SupportedSeedClusteringMethods

DEFAULT_REDUCTION_PERCENTAGE_CLUSTERING = 0.20  # Expected reduction in # of artifacts to # clusters
CLUSTER_ARTIFACT_TYPE = "Cluster"
DEFAULT_REDUCTION_FACTOR = 0.50  # # clusters =  # of artifacts * reduction_factor
DEFAULT_CLUSTER_SIMILARITY_THRESHOLD = 0.5  # Similarity equal or greater will be considered as same clusters
DEFAULT_CLUSTERING_MIN_NEW_ARTIFACTS_RATION = 0.75
DEFAULT_MIN_ORPHAN_SIMILARITY = 0.6  # Minimum similarity score for an oprhan to be placed in a cluster.
DEFAULT_N_NEW_ALLOWED_ARTIFACTS = 2
DEFAULT_RANDOM_STATE = 0
DEFAULT_TESTING_CLUSTERING_METHODS = ["KMEANS", "AGGLOMERATIVE"]
DEFAULT_CLUSTERING_METHODS = ["OPTICS", "SPECTRAL", "AGGLOMERATIVE", "AFFINITY", "KMEANS"]
DEFAULT_ADD_CLUSTERS_TO_DATASET = False
DEFAULT_CLUSTER_MIN_VOTES = 1
DEFAULT_MAX_CLUSTER_SIZE = 10
DEFAULT_FILTER_BY_COHESIVENESS = True
MIN_CLUSTER_SIM_TO_MERGE = 0.7
MIN_ARTIFACT_SIM_TO_MERGE = 0.8
DEFAULT_MIN_CLUSTER_SIZE = 2
DEFAULT_SORT_METRIC = SupportedClusterSortMetrics.SIZE_WEIGHTED_SIM.value
DEFAULT_ALLOW_OVERLAPPING_CLUSTERS = True
NO_CLUSTER_LABEL = -1
MIN_PAIRWISE_SIMILARITY_FOR_CLUSTERING = 0.30
MIN_PAIRWISE_AVG_PERCENTILE = 0.10
ADD_ORPHAN_TO_CLUSTER_THRESHOLD = 0.75
CLUSTERING_SUBDIRECTORY = "clustering"
DEFAULT_SEED_CLUSTERING_METHOD = SupportedSeedClusteringMethods.ARTIFACTS_CHOOSE_CENTROIDS

RANDOM_STATE_PARAM = "random_state"
N_CLUSTERS_PARAM = "n_clusters"
CLUSTER_METHOD_INIT_PARAMS = {
    SupportedClusteringMethods.BIRCH: {
        "branching_factor": DEFAULT_MAX_CLUSTER_SIZE
    },
    SupportedClusteringMethods.OPTICS: {
        "metric": "cosine",
        "min_samples": "[MIN_CLUSTER_SIZE]"
    },
    # SupportedClusteringMethods.HB_SCAN: {
    #     "min_cluster_size": "[MIN_CLUSTER_SIZE]",
    #     "max_cluster_size": "[MAX_CLUSTER_SIZE]"
    # },
    SupportedClusteringMethods.MEANSHIFT: {
        "bandwidth": 2
    },
    SupportedClusteringMethods.SPECTRAL: {
        "assign_labels": "discretize"
    }
}
MIN_ORPHAN_HOME_SIMILARITY = 0.5
ALLOWED_ORPHAN_SIMILARITY_DELTA = 0.1
ALLOWED_ORPHAN_CLUSTER_SIZE_DELTA = 2
DEFAULT_CLUSTER_MAX_SIZE = 5
MIN_SEED_SIMILARITY_QUANTILE = 0.10  # lower percentage of scores to exclude from linking to seeds
UPPER_SEED_SIMILARITY_QUANTILE = 0.95  # percentage of scores to allow to link to multiple parents.
