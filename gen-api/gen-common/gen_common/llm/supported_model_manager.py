from enum import Enum

from gen_common.llm.model_manager import ModelManager


class SupportedModelManager(Enum):
    HF = ModelManager
