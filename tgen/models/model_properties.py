from enum import Enum, IntEnum

from sentence_transformers import SentenceTransformer
from transformers import AutoModel, AutoModelForCausalLM, AutoModelForMaskedLM, AutoModelForSequenceClassification, BertModel

model = BertModel


class AutoModelForSentenceTransformer:
    """
    Creates proxy API for sentence transformers models.
    """

    @staticmethod
    def from_pretrained(model_path: str, **kwargs):
        return SentenceTransformer(model_path)


class ModelTask(Enum):
    SEQUENCE_CLASSIFICATION = AutoModelForSequenceClassification
    MASKED_LEARNING = AutoModelForMaskedLM
    AUTO = AutoModel
    CAUSAL_LM = AutoModelForCausalLM
    SBERT = AutoModelForSentenceTransformer


class ModelArchitectureType(IntEnum):
    SINGLE = 1
    SIAMESE = 2


class ModelSize(Enum):
    SMALL = "small"
    BASE = "base"
    LARGE = "large"
