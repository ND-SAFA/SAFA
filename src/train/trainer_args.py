from typing import Callable, List, Type

import torch
from torch.nn.functional import cross_entropy
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LinearLR, _LRScheduler
from transformers.training_args import TrainingArguments

from config.constants import EVALUATION_STRATEGY_DEFAULT, LOAD_BEST_MODEL_AT_END_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, \
    METRIC_FOR_BEST_MODEL_DEFAULT, N_EPOCHS_DEFAULT, SAVE_STRATEGY_DEFAULT, SAVE_TOTAL_LIMIT_DEFAULT
from train.save_strategy.abstract_save_strategy import AbstractSaveStrategy
from train.save_strategy.epoch_save_strategy import MetricSaveStrategy
from util.base_object import BaseObject


class FunctionalWrapper:
    def __init__(self, f: Callable):
        self.f = f

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


class TrainerArgs(TrainingArguments, BaseObject):
    # required
    output_dir: str

    # Tokenizer
    max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT

    # Trainer
    train_epochs_range: List = None
    num_train_epochs: int = N_EPOCHS_DEFAULT
    checkpoint_path: str = None
    evaluation_strategy: str = EVALUATION_STRATEGY_DEFAULT
    save_strategy: str = SAVE_STRATEGY_DEFAULT
    save_total_limit: int = SAVE_TOTAL_LIMIT_DEFAULT
    load_best_model_at_end: bool = LOAD_BEST_MODEL_AT_END_DEFAULT
    metric_for_best_model_default: str = METRIC_FOR_BEST_MODEL_DEFAULT
    metrics: List[str] = None
    place_model_on_device: bool = False
    total_training_epochs: int = None
    optimizer_constructor: Type[Optimizer] = FunctionalWrapper(torch.optim.Adam)
    loss_function: Callable = FunctionalWrapper(cross_entropy)
    scheduler_constructor: Type[_LRScheduler] = FunctionalWrapper(LinearLR)
    use_custom_train_loop: bool = False
    gradient_accumulation_steps: int = 8
    custom_save_strategy: AbstractSaveStrategy = MetricSaveStrategy(metric_name="map")

    # GAN
    n_hidden_layers_g: int = 1
    n_hidden_layers_d: int = 1
    noise_size: int = 100  # size of the generator's input noisy vectors
    out_dropout_rate: float = 0.9  # dropout to be applied to discriminator's input vectors
    apply_scheduler: bool = False
    epsilon: float = 1e-8
    print_each_n_step: int = 100
    learning_rate_discriminator: float = 5e-5
    learning_rate_generator: float = 5e-5
    warmup_proportion: float = 0.1
    apply_balance: bool = True  # Replicate labeled data to balance poorly represented data,
    shuffle: bool = True

    # Misc
    callbacks: List = None
    multi_gpu: bool = True

    def __init__(self, output_dir: str, **kwargs):
        """
        Arguments for Learning Model
        :param output_dir: dir to save trainer trace_output to
        :param dataset_container: The map containing data for each of the roles used in a model training.
        :param kwargs: optional arguments for Trainer as identified at link below + other class attributes (i.e. resample_rate)
        https://huggingface.co/docs/transformers/v4.21.0/en/main_classes/trainer#transformers.TrainingArguments
        """
        super().__init__(log_level="info", log_level_replica="info", output_dir=output_dir,
                         num_train_epochs=self.num_train_epochs)
        self.__set_args(**kwargs)

    def __set_args(self, **kwargs) -> None:
        """
        Sets class args
        :param kwargs: optional arguments for Trainer
        :return: None
        """
        for arg_name, arg_value in kwargs.items():
            if hasattr(self, arg_name):
                setattr(self, arg_name, arg_value)
            else:
                raise Exception("Unrecognized training arg: " + arg_name)
