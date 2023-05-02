from tgen.util.supported_enum import SupportedEnum


class LLMTask(SupportedEnum):
    """
    Enumerates the types of
    """
    GENERATION = "generation"
    CLASSIFICATION = "classification"
