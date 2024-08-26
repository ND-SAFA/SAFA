from gen_common.util.supported_enum import SupportedEnum


class HealthTask(SupportedEnum):
    CONTRADICTION = "contradictions"
    CONCEPT_EXTRACTION = "concept-extraction"
    CONCEPT_MATCHING = "concept-matching"
