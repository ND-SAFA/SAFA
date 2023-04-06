from enum import Enum


class OpenAITask(Enum):
    CLASSIFICATION = "classification"
    FINE_TUNE = "fine-tune"
    PREDICT = "predict"
