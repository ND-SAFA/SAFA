from enum import Enum


class OpenAITask(Enum):
    FINE_TUNE = "fine-tune"
    PREDICT = "predict"
