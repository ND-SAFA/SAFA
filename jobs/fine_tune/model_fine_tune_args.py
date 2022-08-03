from typing import Dict, List

from transformers.training_args import TrainingArguments
from data.trace_dataset_creator import TraceDatasetCreator
from models.model_generator import ModelGenerator
from constants import RESAMPLE_RATE_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, EVAL_DATASET_SIZE_DEFAULT, PAD_TO_MAX_LENGTH_DEFAULT, \
    LINKED_TARGETS_ONLY_DEFAULT


class ModelFineTuneArgs(TrainingArguments):
    pad_to_max_length: bool = PAD_TO_MAX_LENGTH_DEFAULT
    linked_targets_only: bool = LINKED_TARGETS_ONLY_DEFAULT
    resample_rate: int = RESAMPLE_RATE_DEFAULT
    max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT
    dataset_size: int = EVAL_DATASET_SIZE_DEFAULT
    metrics: List[str] = None

    def __init__(self, model_path: str, output_path: str, s_arts: Dict, t_arts: Dict, links: List, **kwargs):
        """
        Arguments for Learning Model
        :param model_path: location of model
        :param output_path: destination for model
        :param s_arts: source artifacts represented as id, token mappings
        :param t_arts: target artifacts represented as id, token mappings
        :param links: list of tuples containing linked source and target ids
        :param kwargs: optional arguments for Trainer as identified at link below + other class attributes (i.e. resample_rate)
        https://huggingface.co/docs/transformers/v4.21.0/en/main_classes/trainer#transformers.TrainingArguments
        """
        self.output_dir = output_path
        self.__set_args(**kwargs)
        self.model_generator = ModelGenerator(model_path)
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
