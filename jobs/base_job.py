from abc import abstractmethod, ABC
from typing import Union

from jobs.job_args import LMArgs, PretrainArgs
from pretrain.pretrainer import PreTrainer
from jobs.job_result import JobResult
from train.lmtrainer import LMTrainer
from pretrain.electra.configure_pretraining import PretrainingConfig


class BaseJob:

    def __init__(self, args: Union[LMArgs, PretrainingConfig]):
        """
        Base job class
        :param args: job arguments
        """
        self.args = args

    @abstractmethod
    def __start(self) -> JobResult:
        """
        Runs the logic of the specific job
        :return: result of the job
        """
        pass

    def start(self) -> JobResult:
        """
        Starts the job
        :return: result of the job
        """
        return self.__start()


class BaseLMJob(BaseJob, ABC):

    def __init__(self, args: LMArgs):
        """
        Base job for learning model (i.e. training, prediction, evaluation...)
        :param args: arguments used for learning model
        """
        super().__init__(args)
        self.trainer = LMTrainer(args=self.args, model_generator=self.args.model_generator, dataset_creator=self.args.dataset)


class BasePretrainJob(BaseJob, ABC):

    def __init__(self, args: PretrainArgs):
        """
        Base job for pretraining
        :param args: arguments used for pretraining
        """
        super().__init__(args)
        self.pretrain = PreTrainer(args)
