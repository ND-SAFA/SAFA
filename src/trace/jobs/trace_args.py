from typing import List

from transformers.training_args import TrainingArguments

from trace.config.constants import EVAL_DATASET_SIZE_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, \
    PAD_TO_MAX_LENGTH_DEFAULT, RESAMPLE_RATE_DEFAULT
from trace.data.trace_dataset_creator import TraceDatasetCreator
from common.models.model_generator import ModelGenerator


class TraceArgs(TrainingArguments):
    pad_to_max_length: bool = PAD_TO_MAX_LENGTH_DEFAULT
    resample_rate: int = RESAMPLE_RATE_DEFAULT
    max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT
    dataset_size: int = EVAL_DATASET_SIZE_DEFAULT
    metrics: List[str] = None

    def __init__(self, model_generator: ModelGenerator,
                 trace_dataset_creator: TraceDatasetCreator,
                 output_path: str = None, **kwargs):
        """
        Arguments for Learning Model
        :param model_generator: generates model with specified base model and path.
        :param output_path: destination for model
        :param trace_dataset_creator: creates dataset containing traces to train/predict
        :param kwargs: optional arguments for Trainer as identified at link below + other class attributes (i.e. resample_rate)
        https://huggingface.co/docs/transformers/v4.21.0/en/main_classes/trainer#transformers.TrainingArguments
        """
        self.output_dir = output_path
        self.__set_args(**kwargs)
        self.model_generator = model_generator
        self.trace_dataset_creator = trace_dataset_creator

    def __set_args(self, **kwargs) -> None:
        """
        Sets class args
        :param kwargs: optional arguments for Trainer
        :return: None
        """
        for arg_name, arg_value in kwargs.items():
            if hasattr(self, arg_name):
                self.__setattr__(arg_name, arg_value)
