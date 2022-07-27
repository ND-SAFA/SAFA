from typing import Dict, List

from transformers.training_args import TrainingArguments
from data.trace_dataset import TraceDatasetCreator
from models.model_generator import ModelSize
from models.supported_models import MODEL_GENERATORS, SupportedModelIdentifier
from constants import RESAMPLE_RATE_DEFAULT, MAX_SEQ_LENGTH_DEFAULT, EVAL_DATASET_SIZE_DEFAULT, PAD_TO_MAX_LENGTH_DEFAULT, \
    LINKED_TARGETS_ONLY_DEFAULT, PRETRAIN_BATCH_SIZE_DEFAULT, PRETRAIN_DATA_PATH, \
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

    def __init__(self, model_id: SupportedModelIdentifier, s_arts: Dict, t_arts: Dict, links: List, **kwargs):
        """
        Arguments for Learning Model
        :param model_name: name of desired model
        :param s_arts: source artifacts represented as id, token mappings
        :param t_arts: target artifacts represented as id, token mappings
        :param links: list of tuples containing linked source and target ids
        :param kwargs: optional arguments for Trainer as identified at link below + other class attributes (i.e. resample_rate)
        https://huggingface.co/docs/transformers/v4.21.0/en/main_classes/trainer#transformers.TrainingArguments
        """
        self.__set_args(**kwargs)
        self.model_generator = MODEL_GENERATORS[model_id]()
        self.dataset = TraceDatasetCreator(s_arts, t_arts, links, self.model_generator, self.linked_targets_only)

    def __set_args(self, **kwargs) -> None:
        """
        Sets class args
        :param kwargs: optional arguments for Trainer
        :return: None
        """
        for arg_name, arg_value in kwargs.items():
            if hasattr(self, arg_name):
                self.__setattr__(arg_name, arg_value)


class PretrainArgs(PretrainingConfig):
    num_processes: int = 1
    blanks_separate_docs: bool = False
    strip_accents: bool = True
    data_dir = PRETRAIN_DATA_PATH
    model_id: SupportedModelIdentifier = SupportedModelIdentifier.ELECTRA_TRACE_SINGLE
    vocab_file: str = PRETRAIN_VOCAB_FILE
    train_batch_size: int = PRETRAIN_BATCH_SIZE_DEFAULT
    learning_rate: float = PRETRAIN_LEARNING_RATE_DEFAULT

    def __init__(self, model_dir: str, corpus_dir: str = None, domain: Domain = Domain.BASE, model_size: ModelSize = ModelSize.BASE,
                 **kwargs):
        """
        Arguments for Pretraining
        :param model_dir: destination for model
        :param corpus_dir: location of corpus for dataset (if not provided, domain corpus will be used)
        :param domain: the desired domain to use corpus from (may specify corpus dir instead)
        :param model_size: size of model
        :param kwargs: optional arguments for Pretrain Config as identified at link below + other class attributes (i.e. vocab_file)
        https://huggingface.co/docs/transformers/model_doc/electra#transformers.ElectraConfig
        """
        self.model_dir = model_dir
        self.output_dir = self.data_dir
        self.model_generator = MODEL_GENERATORS[self.model_id]
        self.model_generator.model_size = model_size
        if not corpus_dir:
            corpus_dir = get_path(domain)
        self.corpus_dir = corpus_dir
        super().__init__(self.model_generator.get_model_name(), self.data_dir, **kwargs)

    def set_do_train(self, do_train: bool = True) -> None:
        """
        Setter for do_train/do_eval
        :param do_train: if True, sets pretrainer for training, else sets for eval
        :return: None
        """
        self.do_train = do_train
        self.do_eval = not do_train
