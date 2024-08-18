from typing import Callable, Dict, List

from torch.nn.functional import cross_entropy
from transformers.training_args import TrainingArguments

from gen_common.constants.hugging_face_constants import DEFAULT_SAVE_BEST_MODEL, EVALUATION_STRATEGY_DEFAULT, \
    EVAL_ON_EPOCH_DEFAULT, \
    EVAL_STEPS_DEFAULT, \
    GRADIENT_ACCUMULATION_DEFAULT, \
    GREATER_IS_BETTER_DEFAULT, LOAD_BEST_MODEL_AT_END_DEFAULT, LOGGING_STEPS_DEFAULT, LOGGING_STRATEGY_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, \
    METRIC_FOR_BEST_MODEL_DEFAULT, \
    MULTI_GPU_DEFAULT, N_EPOCHS_DEFAULT, \
    SAVE_RANDOM_MODEL_DEFAULT, SAVE_STEPS_DEFAULT, SAVE_STRATEGY_DEFAULT, SAVE_TOTAL_LIMIT_DEFAULT, \
    TRAIN_BATCH_SIZE_DEFAULT, USE_BALANCED_BATCHES_DEFAULT
from gen_common.infra.base_object import BaseObject
from gen_common.traceability.metrics.supported_trace_metric import SupportedTraceMetric
from gen_common.util.dataclass_util import DataclassUtil
from gen_common.util.enum_util import FunctionalWrapper


class HuggingFaceArgs(TrainingArguments, BaseObject):
    # required
    output_dir: str

    # Tokenizer
    max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT

    # Trainer
    dataloader_prefetch_factor = None
    full_determinism = True
    train_epochs_range: List = None
    num_train_epochs: int = N_EPOCHS_DEFAULT
    train_batch_size = TRAIN_BATCH_SIZE_DEFAULT
    checkpoint_path: str = None
    evaluation_strategy: str = EVALUATION_STRATEGY_DEFAULT
    save_strategy: str = SAVE_STRATEGY_DEFAULT
    logging_strategy: str = LOGGING_STRATEGY_DEFAULT
    save_steps = SAVE_STEPS_DEFAULT
    eval_steps: int = EVAL_STEPS_DEFAULT
    logging_steps = LOGGING_STEPS_DEFAULT
    metric_for_best_model: str = METRIC_FOR_BEST_MODEL_DEFAULT
    greater_is_better: bool = GREATER_IS_BETTER_DEFAULT
    save_total_limit: int = SAVE_TOTAL_LIMIT_DEFAULT
    load_best_model_at_end: bool = LOAD_BEST_MODEL_AT_END_DEFAULT
    metrics: List[str] = SupportedTraceMetric.get_keys()
    do_eval: bool = True
    place_model_on_device: bool = True
    total_training_epochs: int = None
    # optimizer_name: str = OPTIMIZER_DEFAULT
    weight_decay = 1e-5
    loss_function: Callable = FunctionalWrapper(cross_entropy)
    # scheduler_name: str = SCHEDULER_DEFAULT
    gradient_accumulation_steps: int = GRADIENT_ACCUMULATION_DEFAULT
    skip_save: bool = False
    use_balanced_batches: bool = USE_BALANCED_BATCHES_DEFAULT
    per_device_train_batch_size = 1
    eval_on_each_epoch: bool = EVAL_ON_EPOCH_DEFAULT
    save_random_model: bool = SAVE_RANDOM_MODEL_DEFAULT
    best_model_path: str = None
    do_training_eval = True
    save_best_model = DEFAULT_SAVE_BEST_MODEL

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

    # Sentence-BERT
    use_scores: bool = False
    st_loss_function = None
    freeze_base: bool = False
    final_learning_rate = 5e-6

    # Misc
    multi_gpu: bool = MULTI_GPU_DEFAULT
    deepspeed_path: str = None
    eager_load_data: bool = False

    def __init__(self, output_dir: str, **kwargs):
        """
        Arguments for Learning Model
        :param output_dir: dir to save trainer output to
        :param dataset_container: The map containing data for each of the roles used in a model training.
        :param kwargs: optional arguments for Trainer as identified at link below + other class attributes (i.e. resample_rate)
        https://huggingface.co/docs/transformers/v4.21.0/en/main_classes/trainer#transformers.TrainingArguments
        """
        super_args = DataclassUtil.set_unique_args(self, TrainingArguments, **kwargs)
        super().__init__(log_level="info", log_level_replica="info", output_dir=output_dir,  # args whose name is different from parent
                         report_to="wandb", deepspeed=self.deepspeed_path, **super_args)

    def __set_unique_args(self, **kwargs) -> Dict:
        """
        Sets arguments that are unique to this class and returns those belonging to super class.
        :param kwargs: Keyword arguments for class.
        :return: Keyword arguments belonging to parent class.
        """
        super_args = {}
        for arg_name, arg_value in kwargs.items():
            if hasattr(super(), arg_name):
                super_args[arg_name] = arg_value
            if hasattr(self, arg_name):
                setattr(self, arg_name, arg_value)
            else:
                raise Exception("Unrecognized training arg: " + arg_name)
        return super_args
