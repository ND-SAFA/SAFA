from gen_common.util.supported_enum import SupportedEnum


class SupportedClusterSortMetrics(SupportedEnum):
    AVG_SIMILARITY = "avg_similarity"
    MIN_SIM = "min_sim"
    MAX_SIM = "max_sim"
    MED_SIM = "med_sim"
    AVG_PAIRWISE_SIM = "avg_pairwise_sim"
    SIZE_WEIGHTED_SIM = "size_weighted_sim"
