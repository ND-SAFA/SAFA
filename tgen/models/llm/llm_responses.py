from dataclasses import dataclass

from typing import Dict, List, Optional, Union


@dataclass
class GenerationResponse:
    """
    The response for a batch of generation request.
    """
    batch_responses: List[str]


@dataclass
class ClassificationItemResponse:
    text: str
    probs: Optional[Dict[str, float]] = None


@dataclass
class ClassificationResponse:
    """
    The response for a batch of classification request.
    """
    batch_responses: List[ClassificationItemResponse]  # string if anthropic, dictionary is openAI.


SupportedLLMResponses = Union[ClassificationResponse, GenerationResponse]
