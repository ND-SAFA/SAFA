from enum import Enum

from cdlib import algorithms

from tgen.util.enum_util import FunctionalWrapper


class SupportedClusteringMethod(Enum):
    LOUVAIN = FunctionalWrapper(lambda dataset_graph: algorithms.louvain(dataset_graph, resolution=1.2))
    WCOMMUNITY = FunctionalWrapper(lambda dataset_graph: algorithms.wCommunity(dataset_graph,
                                                                               min_bel_degree=0.6, threshold_bel_degree=0.6))
    THRESHOLD = FunctionalWrapper(algorithms.threshold_clustering)
