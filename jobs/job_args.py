from typing import Dict, List

from transformers.training_args import TrainingArguments
from data.trace_dataset import TraceDataset
from models.supported_models import MODEL_GENERATORS
from constants import RESAMPLE_RATE_DEFAULT, MAX_SEQ_LENGTH_DEFAULT


# TODO
class JobArgs(TrainingArguments):
    def __init__(self, model_name: str, s_arts: Dict, t_arts: Dict, links: List, pad_to_max_length: bool = True,
                 resample_rate: int = RESAMPLE_RATE_DEFAULT, max_seq_length=MAX_SEQ_LENGTH_DEFAULT):
        self.model_generator = MODEL_GENERATORS[model_name]()
        self.dataset = TraceDataset(s_arts, t_arts, links, self.model_generator)
        self.pad_to_max_length = pad_to_max_length
        self.resample_rate = resample_rate
        self.max_seq_length = max_seq_length
