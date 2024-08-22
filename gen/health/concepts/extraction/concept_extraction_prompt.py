from typing import List

from pydantic.v1 import BaseModel, Field

UNDEFINED_ENTITY_EXTRACTION_PROMPT = (
    "You are given an artifact and list of project concepts found to be used within it. "
    "You're job is to identify important undefined concepts used in the artifact. "
    "These concepts should be specific the domain of the project."
)


class UndefinedEntityExtractionPromptFormat(BaseModel):
    """
    The expected format for undefined concepts found within an artifact.
    """
    undefined_concepts: List[str] = Field(description=["undefined_term_1", "undefined_term_2"])
