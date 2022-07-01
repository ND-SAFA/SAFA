from typing import Dict, List

from transformers.training_args import TrainingArguments
from data.trace_dataset import TraceDataset
from models.supported_models import MODEL_GENERATORS
from constants import RESAMPLE_RATE_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, EVAL_DATASET_SIZE_DEFAULT


# TODO
class JobArgs(TrainingArguments):
    pad_to_max_length = True
    resample_rate = RESAMPLE_RATE_DEFAULT
    max_seq_length = MAX_SEQ_LENGTH_DEFAULT
    dataset_size = EVAL_DATASET_SIZE_DEFAULT

    def __init__(self, model_name: str, s_arts: Dict, t_arts: Dict, links: List, linked_targets_only: bool = False):
        self.model_generator = MODEL_GENERATORS[model_name]()
        self.dataset = TraceDataset(s_arts, t_arts, links, self.model_generator, linked_targets_only)
