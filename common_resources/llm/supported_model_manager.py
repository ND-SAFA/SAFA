from enum import Enum

from common_resources.llm.model_manager import ModelManager


class SupportedModelManager(Enum):
    HF = ModelManager
