from enum import Enum

from models.llm_model_manager import LlmModelManager
from models.model_manager import ModelManager


class SupportedModelManager(Enum):
    BASE = ModelManager
    LLM = LlmModelManager
