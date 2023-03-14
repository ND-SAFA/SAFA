from enum import Enum

from models.llama.modeling_llama import LLaMAForSequenceClassification, LLaMAForSequenceSimilarity


class LLaMATask(Enum):
    SEQUENCE_CLASSIFICATION = LLaMAForSequenceClassification
    SEQUENCE_SIMILARITY = LLaMAForSequenceSimilarity
