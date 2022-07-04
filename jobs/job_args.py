from typing import Dict, List

from transformers.training_args import TrainingArguments
from data.trace_dataset import TraceDataset
from models.supported_models import MODEL_GENERATORS
from constants import RESAMPLE_RATE_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, EVAL_DATASET_SIZE_DEFAULT, PAD_TO_MAX_LENGTH_DEFAULT, \
    LINKED_TARGETS_ONLY_DEFAULT


class JobArgs(TrainingArguments):
    pad_to_max_length: bool = PAD_TO_MAX_LENGTH_DEFAULT
    linked_targets_only: bool = LINKED_TARGETS_ONLY_DEFAULT
    resample_rate: int = RESAMPLE_RATE_DEFAULT
    max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT
    dataset_size: int = EVAL_DATASET_SIZE_DEFAULT

    def __init__(self, model_name: str, s_arts: Dict, t_arts: Dict, links: List, **kwargs):
        self.set_args(**kwargs)
        self.model_generator = MODEL_GENERATORS[model_name]()
        self.dataset = TraceDataset(s_arts, t_arts, links, self.model_generator, self.linked_targets_only)

    def set_args(self, **kwargs):
        for arg_name, arg_value in kwargs.items():
            if hasattr(self, arg_name):
                self.__setattr__(arg_name, arg_value)
