from tgen.common.util.enum_util import FunctionalWrapper
from tgen.common.util.supported_enum import SupportedEnum
from tgen.data.clustering.graph_clustering import GraphClustering


class SupportedClusteringMethod(SupportedEnum):
    MANUAL = None
    GRAPH = FunctionalWrapper(GraphClustering.cluster)
