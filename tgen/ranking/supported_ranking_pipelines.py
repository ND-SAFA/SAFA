from tgen.common.util.supported_enum import SupportedEnum
from tgen.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline
from tgen.ranking.llm_ranking_pipeline import LLMRankingPipeline


class SupportedRankingPipelines(SupportedEnum):
    """
    Enumerates the methods of ranking artifacts to their parents.
    """
    LLM = LLMRankingPipeline
    EMBEDDING = EmbeddingRankingPipeline
