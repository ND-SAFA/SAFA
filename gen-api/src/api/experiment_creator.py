from tgen.util.supported_enum import SupportedEnum


class PredictionJobTypes(SupportedEnum):
    LLM = "openai"
    BASE = "base"


class JobCreator:
    """
    Creates experiment definitions for endpoints.
    """
