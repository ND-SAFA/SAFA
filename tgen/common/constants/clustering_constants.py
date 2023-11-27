from tgen.clustering.methods.supported_clustering_methods import SupportedClusteringMethods

CLUSTER_ARTIFACT_TYPE = "Cluster"
DEFAULT_REDUCTION_FACTOR = 0.50  # # clusters =  # of artifacts * reduction_factor
DEFAULT_CLUSTER_SIMILARITY_THRESHOLD = 0.5  # Similarity equal or greater will be considered as same clusters
DEFAULT_CLUSTERING_MIN_NEW_ARTIFACTS_RATION = 0.75
DEFAULT_MIN_ORPHAN_SIMILARITY = 0.75  # Minimum similarity score for an oprhan to be placed in a cluster.
DEFAULT_N_NEW_ALLOWED_ARTIFACTS = 2
DEFAULT_RANDOM_STATE = 0
DEFAULT_TESTING_CLUSTERING_METHODS = ["KMEANS", "AGGLOMERATIVE"]
DEFAULT_CLUSTERING_METHODS = ["OPTICS", "SPECTRAL", "AGGLOMERATIVE", "AFFINITY", "KMEANS"]
DEFAULT_ADD_CLUSTERS_TO_DATASET = False
DEFAULT_CLUSTER_MIN_VOTES = 1
DEFAULT_MAX_CLUSTER_SIZE = 10
DEFAULT_MIN_CLUSTER_SIZE = 2
NO_CLUSTER_LABEL = -1
MIN_PAIRWISE_SIMILARITY_FOR_CLUSTERING = 0.30
MIN_PAIRWISE_AVG_PERCENTILE = 0.10
ADD_ORPHAN_TO_CLUSTER_THRESHOLD = 0.75
CLUSTERING_SUBDIRECTORY = "clustering"

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
    SupportedClusteringMethods.HB_SCAN: {
        "min_cluster_size": "[MIN_CLUSTER_SIZE]",
        "max_cluster_size": "[MAX_CLUSTER_SIZE]"
    },
    SupportedClusteringMethods.MEANSHIFT: {
        "bandwidth": 2
    },
    SupportedClusteringMethods.SPECTRAL: {
        "assign_labels": "discretize"
    }
}
