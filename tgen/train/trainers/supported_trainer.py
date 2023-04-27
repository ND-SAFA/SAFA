from enum import Enum

from tgen.train.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.train.trainers.llm_trainer import LLMTrainer
from tgen.train.trainers.vsm_trainer import VSMTrainer


class SupportedTrainer(Enum):
    HF = HuggingFaceTrainer
    LLM = LLMTrainer
    VSM = VSMTrainer
