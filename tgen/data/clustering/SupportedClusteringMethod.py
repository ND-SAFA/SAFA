from enum import Enum

from tgen.data.clustering.louvain_clustering_method import LouvainClusteringMethod


class SupportedClusteringMethod(Enum):

    LOUVAIN = LouvainClusteringMethod
