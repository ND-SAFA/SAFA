from tgen.common.util.supported_enum import SupportedEnum
from tgen.core.trainers.hugging_face_trainer import HuggingFaceTrainer
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.sentence_transformer_trainer import SentenceTransformerTrainer
from tgen.core.trainers.sentence_transformer_trainer_mlp import SentenceTransformerTrainerMLP
from tgen.core.trainers.vsm_trainer import VSMTrainer


class SupportedHuggingFaceTrainer(SupportedEnum):
    """
    Enumerates the available trainers for hugging face models.
    """
    HF = HuggingFaceTrainer
    ST = SentenceTransformerTrainer
    ST_MLP = SentenceTransformerTrainerMLP


class SupportedTrainer(SupportedEnum):
    """
    Enumerates the supported trainers for all models.
    """
    HF = HuggingFaceTrainer
    LLM = LLMTrainer
    VSM = VSMTrainer
