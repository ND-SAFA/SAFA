from gen_common.util.supported_enum import SupportedEnum
from gen_common.traceability.ranking import ClusteringRankingPipeline
from gen_common.traceability.ranking import EmbeddingRankingPipeline
from gen_common.traceability.ranking import LLMRankingPipeline
from gen_common.traceability.ranking import SearchPipeline


class SupportedRankingPipelines(SupportedEnum):
    """
    Enumerates the methods of ranking artifacts to their parents.
    """
    LLM = LLMRankingPipeline
    EMBEDDING = EmbeddingRankingPipeline
    SEARCH = SearchPipeline
    CLUSTERING = ClusteringRankingPipeline
