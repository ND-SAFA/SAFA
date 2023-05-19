from tgen.data.clustering.graph_clustering import GraphClustering
from tgen.data.clustering.llm_clustering import LLMClustering
from tgen.util.enum_util import FunctionalWrapper
from tgen.util.supported_enum import SupportedEnum


class SupportedClusteringMethod(SupportedEnum):
    MANUAL = None
    GRAPH = FunctionalWrapper(GraphClustering.cluster)
    LLM = FunctionalWrapper(LLMClustering.cluster)

