from tgen.clustering.methods.kmeans_clustering import KMeansClustering
from tgen.common.util.supported_enum import SupportedEnum


class ClusterMethod(SupportedEnum):
    """
    Enumerates all supporting clustering methods.
    """
    KMEANS = KMeansClustering
