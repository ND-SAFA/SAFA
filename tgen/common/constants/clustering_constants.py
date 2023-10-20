from tgen.clustering.methods.supported_cluster_methods import SupportedClusterMethods

DEFAULT_REDUCTION_FACTOR = 0.50  # Expected reduction in # of artifacts to # clusters
DEFAULT_CLUSTER_SIMILARITY_THRESHOLD = 0.40  # Similarity equal or greater will be considered as same clusters
DEFAULT_RANDOM_STATE = 0
DEFAULT_TESTING_CLUSTERING_METHODS = ["KMEANS", "AGGLOMERATIVE"]
DEFAULT_CLUSTERING_METHODS = ["OPTICS", "SPECTRAL", "AGGLOMERATIVE", "AFFINITY", "KMEANS"]
DEFAULT_ADD_CLUSTERS_TO_DATASET = False
DEFAULT_CLUSTER_MIN_VOTES = 2
MAX_CLUSTER_SIZE = 10
MIN_CLUSTER_SIZE = 1
NO_CLUSTER_LABEL = -1
CLUSTER_METHODS_REQUIRING_N_CLUSTERS = [SupportedClusterMethods.KMEANS,
                                        SupportedClusterMethods.AGGLOMERATIVE,
                                        SupportedClusterMethods.BIRCH,
                                        SupportedClusterMethods.SPECTRAL]
CLUSTER_METHOD_INIT_PARAMS = {
    SupportedClusterMethods.BIRCH: {
        "branching_factor": 2
    },
    SupportedClusterMethods.OPTICS: {
        "min_samples": 2
    },
    SupportedClusterMethods.HB_SCAN: {
        "min_cluster_size": 2,
        "max_cluster_size": MAX_CLUSTER_SIZE
    },
    SupportedClusterMethods.MEANSHIFT: {
        "bandwidth": 2
    },
    SupportedClusterMethods.SPECTRAL: {
        "assign_labels": "discretize",
        "random_state": DEFAULT_RANDOM_STATE
    },
    SupportedClusterMethods.AFFINITY: {
        "random_state": DEFAULT_RANDOM_STATE
    }
}
