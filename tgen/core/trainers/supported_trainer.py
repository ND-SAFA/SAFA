from tgen.common.util.supported_enum import SupportedEnum
from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.vsm_trainer import VSMTrainer


class SupportedTrainer(SupportedEnum):
    HF = HuggingFaceTrainer
    LLM = LLMTrainer
    VSM = VSMTrainer
