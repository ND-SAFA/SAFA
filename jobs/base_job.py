from abc import abstractmethod
from transformers.modeling_utils import PreTrainedModel
from transformers.trainer_utils import set_seed
from jobs.job_args import JobArgs
from models.supported_models import MODEL_GENERATORS
from trainer.lmtrainer import LMTrainer


class BaseJob:

    def __init__(self, args: JobArgs):
        self.args = args

    def _get_trainer(self) -> LMTrainer:
        model = self.args.model_generator.load_model()
        data = self.args.dataset.get_training_data()
        return LMTrainer(args=self.args, model=model, dataset=data)

    @abstractmethod
    def _start(self):
        pass

    def start(self):
        set_seed(self.args.seed)
        self._start()
