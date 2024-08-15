from common_resources.tools.util.supported_enum import SupportedEnum
from tgen.tracing.ranking.clustering_ranking_pipeline import ClusteringRankingPipeline
from tgen.tracing.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline
from tgen.tracing.ranking.llm_ranking_pipeline import LLMRankingPipeline
from tgen.tracing.ranking.search_pipeline import SearchPipeline


class SupportedRankingPipelines(SupportedEnum):
    """
    Enumerates the methods of ranking artifacts to their parents.
    """
    LLM = LLMRankingPipeline
    EMBEDDING = EmbeddingRankingPipeline
    SEARCH = SearchPipeline
    CLUSTERING = ClusteringRankingPipeline
