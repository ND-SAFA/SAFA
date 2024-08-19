from gen_common.traceability.ranking.clustering_ranking_pipeline import ClusteringRankingPipeline
from gen_common.traceability.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline
from gen_common.traceability.ranking.llm_ranking_pipeline import LLMRankingPipeline
from gen_common.traceability.ranking.search_pipeline import SearchPipeline
from gen_common.util.supported_enum import SupportedEnum


class SupportedRankingPipelines(SupportedEnum):
    """
    Enumerates the methods of ranking artifacts to their parents.
    """
    LLM = LLMRankingPipeline
    EMBEDDING = EmbeddingRankingPipeline
    SEARCH = SearchPipeline
    CLUSTERING = ClusteringRankingPipeline
