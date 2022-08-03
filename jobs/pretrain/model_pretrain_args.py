from constants import PRETRAIN_BATCH_SIZE_DEFAULT, PRETRAIN_DATA_PATH, PRETRAIN_LEARNING_RATE_DEFAULT, \
    PRETRAIN_VOCAB_FILE
from models.abstract_model_generator import ModelSize
from models.supported_models import MODEL_GENERATORS, SupportedModelIdentifier
from pretrain.corpuses.domain import Domain, get_path
from pretrain.electra.configure_pretraining import PretrainingConfig


class ModelPretrainArgs(PretrainingConfig):
    num_processes: int = 1
    blanks_separate_docs: bool = False
    strip_accents: bool = True
    data_dir = PRETRAIN_DATA_PATH
    model_id: SupportedModelIdentifier = SupportedModelIdentifier.ELECTRA_TRACE_SINGLE
    vocab_file: str = PRETRAIN_VOCAB_FILE
    train_batch_size: int = PRETRAIN_BATCH_SIZE_DEFAULT
    learning_rate: float = PRETRAIN_LEARNING_RATE_DEFAULT

    def __init__(self, model_dir: str, corpus_dir: str = None, domain: Domain = Domain.BASE,
                 model_size: ModelSize = ModelSize.BASE,
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
