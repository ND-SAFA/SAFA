from enum import Enum

from models.llama.llama_model_manager import LLaMAModelManager
from models.model_manager import ModelManager


class SupportedModelManager(Enum):
    BASE = ModelManager
    LLAMA = LLaMAModelManager
