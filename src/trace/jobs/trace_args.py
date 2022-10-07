from typing import Dict, List, Tuple

from transformers.training_args import TrainingArguments

from common.models.model_generator import ModelGenerator
from trace.config.constants import EVAL_DATASET_SIZE_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, \
    N_EPOCHS_DEFAULT, PAD_TO_MAX_LENGTH_DEFAULT, RESAMPLE_RATE_DEFAULT, VALIDATION_PERCENTAGE_DEFAULT
from trace.data.trace_dataset_creator import TraceDatasetCreator


class TraceArgs(TrainingArguments):
    pad_to_max_length: bool = PAD_TO_MAX_LENGTH_DEFAULT
    resample_rate: int = RESAMPLE_RATE_DEFAULT
    max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT
    eval_dataset_size: int = EVAL_DATASET_SIZE_DEFAULT
    validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT
    num_train_epochs: int = N_EPOCHS_DEFAULT
    metrics: List[str] = None
    callbacks: List = None
    pretraining_data_dir: str = None

    def __init__(self, model_generator: ModelGenerator, output_dir: str,
                 trace_dataset_creator: TraceDatasetCreator,
                 source_layers: List[Dict[str, str]] = None,
                 target_layers: List[Dict[str, str]] = None, links: List[Tuple[str, str]] = None,
                 pretraining_data_path: str = None, **kwargs):
        """
        Arguments for Learning Model
        :param model_generator: generates model with specified base model and path.
        :param output_dir: destination for model
        :param source_layers: a list of source artifacts across all layers
        :param target_layers: a list of target artifacts across all layers
        :param links: list of tuples containing linked source and target ids
        :param kwargs: optional arguments for Trainer as identified at link below + other class attributes (i.e. resample_rate)
        https://huggingface.co/docs/transformers/v4.21.0/en/main_classes/trainer#transformers.TrainingArguments
        """
        self.model_generator = model_generator
        self.pretraining_data_path = pretraining_data_path
        self.__set_args(**kwargs)
        super().__init__(log_level="info", log_level_replica="info", output_dir=output_dir,
                         num_train_epochs=self.num_train_epochs)
        self.trace_dataset_creator = TraceDatasetCreator(source_layers=source_layers, target_layers=target_layers,
                                                         true_links=links, model_generator=model_generator,
                                                         validation_percentage=self.validation_percentage) \
            if source_layers and target_layers else None
        if trace_dataset_creator:
            self.trace_dataset_creator = trace_dataset_creator

    def __set_args(self, kwargs) -> None:
        """
        Sets class args
        :param kwargs: optional arguments for Trainer
        :return: None
        """
        for arg_name, arg_value in kwargs.items():
            if hasattr(self, arg_name):
                setattr(self, arg_name, arg_value)
            else:
                print("Unrecognized training arg: ", arg_name)
