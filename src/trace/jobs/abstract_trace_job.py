from abc import ABC

from common.jobs.abstract_args_builder import AbstractArgsBuilder
from common.jobs.abstract_job import AbstractJob
from trace.train.trace_trainer import TraceTrainer


class AbstractTraceJob(AbstractJob, ABC):

    def __init__(self, args_builder: AbstractArgsBuilder, output_dir: str = None, save_output: bool = True):
        """
        Base job for task using a model (i.e. training, prediction, evaluation...)
        :param args_builder: arguments used for configuring the model
        :param output_dir: where to save the results (if not provided, defaults to job_id dir inside output_dir provided in args)
        :param save_output: if True, saves the output of the job
        """
        super().__init__(args_builder, output_dir, save_output)
        self.__trainer = None

    def get_trainer(self) -> TraceTrainer:
        if self.__trainer is None:
            self.__trainer = TraceTrainer(args=self.args)
        return self.__trainer
