from abc import ABC

from common.jobs.abstract_job import AbstractJob
from common.jobs.arg_builder import ArgBuilder
from trace.train.trace_trainer import TraceTrainer


class AbstractTraceJob(AbstractJob, ABC):

    def __init__(self, args_builder: ArgBuilder):
        """
        Base job for task using a model (i.e. training, prediction, evaluation...)
        :param args: arguments used for configuring the model
        """
        super().__init__(args_builder)
        self.trainer = TraceTrainer(args=self.args)
