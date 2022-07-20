from abc import abstractmethod
from jobs.job_args import JobArgs
from trainer.lmtrainer import LMTrainer


class BaseJob:

    def __init__(self, args: JobArgs):
        self.args = args

    @abstractmethod
    def __start(self):
        pass

    def _get_trainer(self) -> LMTrainer:
        return LMTrainer(args=self.args, model_generator=self.args.model_generator, dataset=self.args.dataset)

    def start(self):
        self.__start()
