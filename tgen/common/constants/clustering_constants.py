from tgen.clustering.methods.supported_clustering_methods import SupportedClusteringMethods

DEFAULT_REDUCTION_FACTOR = 0.20  # Expected reduction in # of artifacts to # clusters
DEFAULT_CLUSTER_SIMILARITY_THRESHOLD = 0.6  # Similarity equal or greater will be considered as same clusters
DEFAULT_N_NEW_ALLOWED_ARTIFACTS = 2
DEFAULT_RANDOM_STATE = 0
DEFAULT_TESTING_CLUSTERING_METHODS = ["KMEANS", "AGGLOMERATIVE"]
DEFAULT_CLUSTERING_METHODS = ["OPTICS", "SPECTRAL", "AGGLOMERATIVE", "AFFINITY", "KMEANS"]
DEFAULT_ADD_CLUSTERS_TO_DATASET = False
DEFAULT_CLUSTER_MIN_VOTES = 2
MAX_CLUSTER_SIZE = 10
MIN_CLUSTER_SIZE = 1
NO_CLUSTER_LABEL = -1
CLUSTER_METHODS_REQUIRING_N_CLUSTERS = [SupportedClusteringMethods.KMEANS,
                                        SupportedClusteringMethods.AGGLOMERATIVE,
                                        SupportedClusteringMethods.BIRCH,
                                        SupportedClusteringMethods.SPECTRAL]
CLUSTER_METHOD_INIT_PARAMS = {
    SupportedClusteringMethods.BIRCH: {
        "branching_factor": 2
    },
    SupportedClusteringMethods.OPTICS: {
        "min_samples": 2
    },
    SupportedClusteringMethods.HB_SCAN: {
        "min_cluster_size": 2,
        "max_cluster_size": MAX_CLUSTER_SIZE
    },
    SupportedClusteringMethods.MEANSHIFT: {
        "bandwidth": 2
    },
    SupportedClusteringMethods.SPECTRAL: {
        "assign_labels": "discretize"
    }
}
