from typing import List

from transformers.training_args import TrainingArguments

from config.constants import EVALUATION_STRATEGY_DEFAULT, EVAL_DATASET_SIZE_DEFAULT, LOAD_BEST_MODEL_AT_END_DEFAULT, \
    MAX_SEQ_LENGTH_DEFAULT, METRIC_FOR_BEST_MODEL_DEFAULT, N_EPOCHS_DEFAULT, \
    PAD_TO_MAX_LENGTH_DEFAULT, RESAMPLE_RATE_DEFAULT, SAVE_STRATEGY_DEFAULT, SAVE_TOTAL_LIMIT_DEFAULT, \
    VALIDATION_PERCENTAGE_DEFAULT


class TraceArgs(TrainingArguments):
    # Tokenizer
    pad_to_max_length: bool = PAD_TO_MAX_LENGTH_DEFAULT
    resample_rate: int = RESAMPLE_RATE_DEFAULT
    max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT
    # Training
    num_train_epochs: int = N_EPOCHS_DEFAULT
    validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT
    # Evaluation
    eval_dataset_size: int = EVAL_DATASET_SIZE_DEFAULT
    evaluation_strategy: str = EVALUATION_STRATEGY_DEFAULT
    save_strategy: str = SAVE_STRATEGY_DEFAULT
    save_total_limit: int = SAVE_TOTAL_LIMIT_DEFAULT
    load_best_model_at_end: bool = LOAD_BEST_MODEL_AT_END_DEFAULT
    metric_for_best_model_default: str = METRIC_FOR_BEST_MODEL_DEFAULT
    metrics: List[str] = None
    # GAN
    n_hidden_layers_g = 1
    n_hidden_layers_d = 1
    noise_size = 100  # size of the generator's input noisy vectors
    out_dropout_rate = 0.9  # dropout to be applied to discriminator's input vectors
    apply_scheduler = False
    epsilon = 1e-8
    print_each_n_step = 100
    learning_rate_discriminator = 5e-5
    learning_rate_generator = 5e-5
    warmup_proportion = 0.1
    apply_balance = True  # Replicate labeled data to balance poorly represented datasets,
    shuffle = True
    # Misc
    callbacks: List = None
    multi_gpu = True

    def __init__(self, output_dir, **kwargs):
        """
        Arguments for Learning Model\
        :param kwargs: optional arguments for Trainer as identified at link below + other class attributes (i.e. resample_rate)
        https://huggingface.co/docs/transformers/v4.21.0/en/main_classes/trainer#transformers.TrainingArguments
        """
        self.__set_args(**kwargs)
        super().__init__(log_level="info", log_level_replica="info", output_dir=output_dir,
                         num_train_epochs=self.num_train_epochs)

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
