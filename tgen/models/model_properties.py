from enum import Enum, IntEnum

from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import AutoModel, AutoModelForCausalLM, AutoModelForMaskedLM, AutoModelForSequenceClassification, BertModel

model = BertModel


class AutoModelForSentenceTransformer:

    @staticmethod
    def from_pretrained(model_path: str, **kwargs) -> SentenceTransformer:
        """
        Creates proxy API for sentence transformers models.
        :param model_path: The path to the sentence transformer model.
        :param kwargs: Ignored. Allows ST to confirm to API.
        :return: Sentence transformer model.
        """
        return SentenceTransformer(model_path)


class ModelTask(Enum):
    SEQUENCE_CLASSIFICATION = AutoModelForSequenceClassification
    MASKED_LEARNING = AutoModelForMaskedLM
    AUTO = AutoModel
    CAUSAL_LM = AutoModelForCausalLM
    SBERT = AutoModelForSentenceTransformer
    SENTENCE_TRANSFORMER = SentenceTransformer
    CROSS_ENCODER = CrossEncoder


class ModelArchitectureType(IntEnum):
    SINGLE = 1
    SIAMESE = 2


class ModelSize(Enum):
    SMALL = "small"
    BASE = "base"
    LARGE = "large"
