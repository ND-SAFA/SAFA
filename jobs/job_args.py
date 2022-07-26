from typing import Dict, List, Union

from transformers.training_args import TrainingArguments
from data.trace_dataset import TraceDataset
from models.model_generator import ModelSize
from models.supported_models import MODEL_GENERATORS, SupportedModels
from constants import RESAMPLE_RATE_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, EVAL_DATASET_SIZE_DEFAULT, PAD_TO_MAX_LENGTH_DEFAULT, \
    LINKED_TARGETS_ONLY_DEFAULT, PRETRAIN_NUM_TRAINING_SIZE_DEFAULT, PRETRAIN_BATCH_SIZE_DEFAULT, PRETRAIN_DATA_PATH, \
    PRETRAIN_VOCAB_FILE, PRETRAIN_LEARNING_RATE_DEFAULT

from pretrain.electra.configure_pretraining import PretrainingConfig
from pretrain.corpuses.domain import get_path, Domain


class LMArgs(TrainingArguments):
    pad_to_max_length: bool = PAD_TO_MAX_LENGTH_DEFAULT
    linked_targets_only: bool = LINKED_TARGETS_ONLY_DEFAULT
    resample_rate: int = RESAMPLE_RATE_DEFAULT
    max_seq_length: int = MAX_SEQ_LENGTH_DEFAULT
    dataset_size: int = EVAL_DATASET_SIZE_DEFAULT
    metrics: List[str] = None

    def __init__(self, model_name: str, s_arts: Dict, t_arts: Dict, links: List, **kwargs):
        self.__set_args(**kwargs)
        self.model_generator = MODEL_GENERATORS[model_name]()
        self.dataset = TraceDataset(s_arts, t_arts, links, self.model_generator, self.linked_targets_only)

    def __set_args(self, **kwargs):
        for arg_name, arg_value in kwargs.items():
            if hasattr(self, arg_name):
                self.__setattr__(arg_name, arg_value)


class PretrainArgs(PretrainingConfig):
    num_processes: int = 1
    blanks_separate_docs: bool = False
    strip_accents: bool = True
    data_dir = PRETRAIN_DATA_PATH
    model_generator_name = SupportedModels.ELECTRA_TRACE_SINGLE.value
    vocab_file: str = PRETRAIN_VOCAB_FILE
    train_batch_size: int = PRETRAIN_BATCH_SIZE_DEFAULT
    learning_rate: float = PRETRAIN_LEARNING_RATE_DEFAULT

    def __init__(self, model_dir: str, corpus_dir: str = None, model_size: str = ModelSize.BASE.value, **kwargs):
        self.model_dir = model_dir
        self.output_dir = self.data_dir
        self.model_generator = MODEL_GENERATORS[self.model_generator_name]
        self.model_generator.model_size = model_size
        if not corpus_dir:
            corpus_dir = get_path(Domain.BASE.value)
        self.corpus_dir = corpus_dir
        super().__init__(self.model_generator.get_model_name(), self.data_dir, **kwargs)

    def set_do_train(self, do_train=True):
        self.do_train = do_train
        self.do_eval = not do_train
