from transformers.training_args import TrainingArguments
from data.trace_data import TraceData


# TODO
class JobArgs(TrainingArguments):
    def __init__(self, model_name: str, data: TraceData, pad_to_max_length: bool = True):
        self.pad_to_max_length = pad_to_max_length
        self.model_name = model_name
        self.data = data
