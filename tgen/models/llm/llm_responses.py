from dataclasses import dataclass

from typing import List, Union


@dataclass
class GenerationResponse:
    """
    The response for a batch of generation request.
    """
    batch_responses: List[str]


@dataclass
class ClassificationResponse:
    """
    The response for a batch of classification request.
    """
    batch_responses: List[str]


SupportedLLMResponses = Union[ClassificationResponse, GenerationResponse]
