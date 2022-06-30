from typing import Dict, List

from transformers.training_args import TrainingArguments
from data.trace_dataset import TraceDataset
from models.supported_models import MODEL_GENERATORS


# TODO
class JobArgs(TrainingArguments):
    def __init__(self, model_name: str, s_arts: Dict, t_arts: Dict, links: List, pad_to_max_length: bool = True):
        self.pad_to_max_length = pad_to_max_length
        self.model_generator = MODEL_GENERATORS[model_name]()
        self.dataset = TraceDataset(s_arts, t_arts, links, self.model_generator)
