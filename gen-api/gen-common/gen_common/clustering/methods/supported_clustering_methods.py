# from hdbscan import HDBSCAN
from sklearn.cluster import AffinityPropagation, AgglomerativeClustering, Birch, DBSCAN, KMeans, MeanShift, OPTICS, SpectralClustering

from gen_common.util.supported_enum import SupportedEnum


class SupportedClusteringMethods(SupportedEnum):
    """
    Enumerates all supporting clustering methods.
    """
    BIRCH = Birch  # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.Birch.html#sklearn.cluster.Birch
    KMEANS = KMeans
    AGGLOMERATIVE = AgglomerativeClustering
    OPTICS = OPTICS  # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.OPTICS.html#sklearn.cluster.OPTICS
    #  HB_SCAN = HDBSCAN  # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html#sklearn.cluster.HDBSCAN
    DBSCAN = DBSCAN  # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN
    MEANSHIFT = MeanShift
    SPECTRAL = SpectralClustering
    AFFINITY = AffinityPropagation
