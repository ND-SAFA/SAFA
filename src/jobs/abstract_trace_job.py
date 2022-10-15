from abc import ABC

from jobs.abstract_args_builder import AbstractArgsBuilder
from jobs.abstract_job import AbstractJob
from train.trace_trainer import TraceTrainer


class AbstractTraceJob(AbstractJob, ABC):

    def __init__(self, args_builder: AbstractArgsBuilder):
        """
        Base job for task using a model (i.e. training, prediction, evaluation...)
        :param args_builder: arguments used for configuring the model
        """
        super().__init__(args_builder)
        self.__trainer = None

    def get_trainer(self, **kwargs) -> TraceTrainer:
        if self.__trainer is None:
            self.__trainer = TraceTrainer(args=self.args, **kwargs)
        return self.__trainer
