from typing import Dict, List

from transformers import TrainingArguments

from constants import EVAL_DATASET_SIZE_DEFAULT, LINKED_TARGETS_ONLY_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, \
    PAD_TO_MAX_LENGTH_DEFAULT, \
    RESAMPLE_RATE_DEFAULT
from data.trace_dataset_creator import TraceDatasetCreator
from models.supported_models import MODEL_GENERATORS, SupportedModelIdentifier


class ModelTrainingArgs(TrainingArguments):
    pad_to_max_length: bool = PAD_TO_MAX_LENGTH_DEFAULT
    linked_targets_only: bool = LINKED_TARGETS_ONLY_DEFAULT
    resample_rate: int = RESAMPLE_RATE_DEFAULT
    max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT
    dataset_size: int = EVAL_DATASET_SIZE_DEFAULT
    metrics: List[str] = None

    def __init__(self, model_id: SupportedModelIdentifier, s_arts: Dict, t_arts: Dict, links: List, **kwargs):
        """
        Arguments for Learning Model
        :param model_name: name of desired model
        :param s_arts: source artifacts represented as id, token mappings
        :param t_arts: target artifacts represented as id, token mappings
        :param links: list of tuples containing linked source and target ids
        :param kwargs: optional arguments for Trainer as identified at link below + other class attributes (i.e. resample_rate)
        https://huggingface.co/docs/transformers/v4.21.0/en/main_classes/trainer#transformers.TrainingArguments
        """
        self.__set_args(**kwargs)
        self.model_generator = MODEL_GENERATORS[model_id]()
        self.dataset = TraceDatasetCreator(s_arts, t_arts, links, self.model_generator, self.linked_targets_only)

    def __set_args(self, **kwargs) -> None:
        """
        Sets class args
        :param kwargs: optional arguments for Trainer
        :return: None
        """
        for arg_name, arg_value in kwargs.items():
            if hasattr(self, arg_name):
                self.__setattr__(arg_name, arg_value)
