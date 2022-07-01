from abc import abstractmethod
from transformers.modeling_utils import PreTrainedModel
from transformers.trainer_utils import set_seed
from jobs.job_args import JobArgs
from trainer.lmtrainer import LMTrainer


class BaseJob:

    def __init__(self, args: JobArgs):
        self.args = args

    @abstractmethod
    def _start(self):
        pass

    def _get_trainer(self) -> LMTrainer:
        return LMTrainer(args=self.args, model_generator=self.args.model_generator, dataset=self.args.dataset)

    def start(self):
        set_seed(self.args.seed)
        self._start()
