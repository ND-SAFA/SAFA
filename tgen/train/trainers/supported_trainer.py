from enum import Enum

from tgen.train.trainers.ai_trainer import AITrainer
from tgen.train.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.train.trainers.vsm_trainer import VSMTrainer


class SupportedTrainer(Enum):
    HF = HuggingFaceTrainer
    OPEN_AI = AITrainer
    VSM = VSMTrainer
