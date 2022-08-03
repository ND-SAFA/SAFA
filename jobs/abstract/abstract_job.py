from abc import abstractmethod
from typing import Union

from jobs.abstract.job_result import JobResult
from jobs.fine_tune.model_fine_tune_args import ModelFineTuneArgs
from pretrain.electra.configure_pretraining import PretrainingConfig


class AbstractJob:

    def __init__(self, args: Union[ModelFineTuneArgs, PretrainingConfig]):
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
