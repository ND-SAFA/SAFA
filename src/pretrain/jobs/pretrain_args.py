from pretrain.config.constants import PRETRAIN_BATCH_SIZE_DEFAULT, PRETRAIN_LEARNING_RATE_DEFAULT, \
    PRETRAIN_MODEL_NAME, PRETRAIN_VOCAB_FILE
from pretrain.config.paths import PRETRAIN_DATA_PATH
from common.models.model_generator import ModelGenerator
from pretrain.data.corpuses.domain import Domain, get_path
from pretrain.electra.configure_pretraining import PretrainingConfig


class ModelPretrainArgs(PretrainingConfig):
    num_processes: int = 1
    blanks_separate_docs: bool = False
    strip_accents: bool = True
    data_dir = PRETRAIN_DATA_PATH
    vocab_file: str = PRETRAIN_VOCAB_FILE
    train_batch_size: int = PRETRAIN_BATCH_SIZE_DEFAULT
    learning_rate: float = PRETRAIN_LEARNING_RATE_DEFAULT

    def __init__(self, model_generator: ModelGenerator, output_path: str,
                 corpus_dir: str = None, domain: Domain = Domain.BASE, **kwargs):
        """
        Arguments for Pretraining
        :param model_generator: generates model and path to checkpoint
        :param output_path: destination for model
        :param domain: the desired domain to use corpus from (may specify corpus dir instead)
        :param corpus_dir: location of corpus for dataset (if not provided, domain corpus will be used)
        :param model_size: size of model
        :param kwargs: optional arguments for Pretrain Config as identified at link below + other class attributes (i.e. vocab_file)
        https://huggingface.co/docs/transformers/model_doc/electra#transformers.ElectraConfig
        """
        self.output_dir = output_path
        if corpus_dir is None:
            corpus_dir = get_path(domain)
        self.corpus_dir = corpus_dir
        model_size = model_generator.model_size
        model_path = model_generator.model_path
        super().__init__(PRETRAIN_MODEL_NAME.format(model_size.value), self.data_dir, model_dir=model_path,
                         model_size=model_size.value, **kwargs)
        self.model_generator = model_generator

    def set_do_train(self, do_train: bool = True) -> None:
        """
        Setter for do_train/do_eval
        :param do_train: if True, sets pretrainer for training, else sets for eval
        :return: None
        """
        self.do_train = do_train
        self.do_eval = not do_train
