from enum import IntEnum, Enum
from transformers import AutoModelForMaskedLM, AutoModelForSequenceClassification

from models.distill.distill_models import TinyBertForSequenceClassification


class ModelTask(Enum):
    SEQUENCE_CLASSIFICATION = AutoModelForSequenceClassification
    MASKED_LEARNING = AutoModelForMaskedLM
    DISTILL = TinyBertForSequenceClassification


class ModelArchitectureType(IntEnum):
    SINGLE = 1
    SIAMESE = 2


class ModelSize(Enum):
    SMALL = "small"
    BASE = "base"
    LARGE = "large"
