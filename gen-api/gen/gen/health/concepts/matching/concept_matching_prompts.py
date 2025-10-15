from typing import List

from pydantic.v1 import BaseModel, Field

LLM_CONCEPT_MATCHING_SYSTEM_PROMPT = (
    "You will be given a list of project-specific concepts and terminology "
    "alongside a specific target artifact from the project. "
    "Your job is to note which artifact IDs are referenced in the target artifact text. "
    "Only include predictions which have a direct reference to the concept/terminology in the target artifact text. "
    "Only provide the IDs of the concepts / terminology that are referenced in the target artifact text. "
    "Only provide the content specified in the format instructions."
    "If no concept IDs are found to be referenced, use empty list for predictions."
)


class LLMConceptMatchingPredictionFormat(BaseModel):
    """
    Prediction that a concept is contained within target artifact.
    """
    artifact_id: str = Field(description="The artifact ID of the concept referenced.")
    explanation: str = Field(description="Explanation of where the target artifact references concept.")


class LLMConceptMatchingPromptFormat(BaseModel):
    """
    Response for making predictions for cited concepts in target artifact.
    """
    predictions: List[dict] = Field(description=[
        {
            "artifact_id": "reference_concept_1",
            "explanation": "where concept_1 is referenced in artifact"
        },
        {
            "artifact_id": "reference_concept_2",
            "explanation": "where concept_2 is referenced in artifact"
        },
    ]
    )
