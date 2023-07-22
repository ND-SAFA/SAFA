from tgen.common.util.enum_util import FunctionalWrapper
from tgen.common.util.supported_enum import SupportedEnum
from tgen.data.clustering.graph_clustering import GraphClustering
from tgen.data.clustering.llm_clustering import LLMClustering


class SupportedClusteringMethod(SupportedEnum):
    MANUAL = None
    GRAPH = FunctionalWrapper(GraphClustering.cluster)
    LLM = FunctionalWrapper(LLMClustering.cluster)
