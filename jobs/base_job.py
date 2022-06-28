from abc import abstractmethod
from typing import Dict
from transformers.modeling_utils import PreTrainedModel
from transformers.trainer_utils import set_seed
from jobs.job_args import JobArgs
from models.supported_models import MODEL_IDENTIFIERS
from transformers import AutoConfig, AutoTokenizer, default_data_collator, DataCollatorWithPadding
from train.trainer import LMTrainer


class BaseJob:

    def __init__(self, args: JobArgs):
        self.args = args
        self.model_identifier = MODEL_IDENTIFIERS[self.args.model_name]()

    def _load_model(self) -> PreTrainedModel:
        config = AutoConfig.from_pretrained(self.model_identifier.model_path)
        config.num_labels = 2
        return self.model_identifier.model_class.from_pretrained(self.model_identifier.model_path, config=config)

    def _get_trainer(self) -> LMTrainer:
        model = self._load_model()
        tokenizer = AutoTokenizer.from_pretrained(self.model_identifier.model_path)
        dataset = self.args.data.make_dataset(tokenizer, self.args)
        return LMTrainer(args=self.args, model=model, dataset=dataset)

    @abstractmethod
    def _start(self, trainer: LMTrainer):
        pass

    def start(self):
        set_seed(self.args.seed)
        trainer = self._get_trainer()
        self._start(trainer)
