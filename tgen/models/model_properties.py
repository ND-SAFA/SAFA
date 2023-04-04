from enum import Enum, IntEnum

from transformers import AutoModel, AutoModelForCausalLM, AutoModelForMaskedLM, AutoModelForSequenceClassification


class ModelTask(Enum):
    SEQUENCE_CLASSIFICATION = AutoModelForSequenceClassification
    MASKED_LEARNING = AutoModelForMaskedLM
    AUTO = AutoModel
    CAUSAL_LM = AutoModelForCausalLM


class ModelArchitectureType(IntEnum):
    SINGLE = 1
    SIAMESE = 2


class ModelSize(Enum):
    SMALL = "small"
    BASE = "base"
    LARGE = "large"
