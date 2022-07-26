from abc import abstractmethod, ABC
from typing import Union

from jobs.job_args import LMArgs, PretrainArgs
from pretrain.pretrainer import Pretrainer
from train.lmtrainer import LMTrainer
from pretrain.electra.configure_pretraining import PretrainingConfig


class BaseJob:

    def __init__(self, args: Union[LMArgs, PretrainingConfig]):
        self.args = args

    @abstractmethod
    def __start(self):
        pass

    def start(self):
        self.__start()


class BaseLMJob(BaseJob, ABC):

    def __init__(self, args: LMArgs):
        super().__init__(args)
        self.trainer = LMTrainer(args=self.args, model_generator=self.args.model_generator, dataset=self.args.dataset)


class BasePretrainJob(BaseJob, ABC):

    def __init__(self, args: PretrainArgs):
        super().__init__(args)
        self.pretrain = Pretrainer(args)
