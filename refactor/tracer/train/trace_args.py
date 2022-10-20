from typing import List
import datasets
from transformers.training_args import TrainingArguments

from config.constants import EVAL_DATASET_SIZE_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, \
    N_EPOCHS_DEFAULT, PAD_TO_MAX_LENGTH_DEFAULT, RESAMPLE_RATE_DEFAULT, VALIDATION_PERCENTAGE_DEFAULT, EVALUATION_STRATEGY_DEFAULT, \
    SAVE_STRATEGY_DEFAULT, SAVE_TOTAL_LIMIT_DEFAULT, LOAD_BEST_MODEL_AT_END_DEFAULT, METRIC_FOR_BEST_MODEL_DEFAULT


class TraceArgs(TrainingArguments):
    pad_to_max_length: bool = PAD_TO_MAX_LENGTH_DEFAULT
    resample_rate: int = RESAMPLE_RATE_DEFAULT
    max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT
    eval_dataset_size: int = EVAL_DATASET_SIZE_DEFAULT
    validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT
    num_train_epochs: int = N_EPOCHS_DEFAULT
    evaluation_strategy: str = EVALUATION_STRATEGY_DEFAULT
    save_strategy: str = SAVE_STRATEGY_DEFAULT
    save_total_limit: int = SAVE_TOTAL_LIMIT_DEFAULT
    load_best_model_at_end: bool = LOAD_BEST_MODEL_AT_END_DEFAULT
    metric_for_best_model_default: str = METRIC_FOR_BEST_MODEL_DEFAULT
    metrics: List[str] = None
    callbacks: List = None

    def __init__(self, output_dir, **kwargs):
        """
        Arguments for Learning Model\
        :param kwargs: optional arguments for Trainer as identified at link below + other class attributes (i.e. resample_rate)
        https://huggingface.co/docs/transformers/v4.21.0/en/main_classes/trainer#transformers.TrainingArguments
        """
        self.__set_args(**kwargs)
        super().__init__(log_level="info", log_level_replica="info", output_dir=output_dir,
                         num_train_epochs=self.num_train_epochs)

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
