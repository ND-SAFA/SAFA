from enum import IntEnum, Enum
from transformers import AutoModelForMaskedLM, AutoModelForSequenceClassification


class ModelTask(Enum):
    SEQUENCE_CLASSIFICATION = AutoModelForSequenceClassification
    MASKED_LEARNING = AutoModelForMaskedLM


class ModelArchitectureType(IntEnum):
    SINGLE = 1
    SIAMESE = 2


class ModelSize(Enum):
    SMALL = "small"
    BASE = "base"
    LARGE = "large"
