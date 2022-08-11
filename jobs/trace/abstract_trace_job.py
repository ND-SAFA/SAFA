from abc import ABC

from jobs.common.abstract_job import AbstractJob
from jobs.trace.trace_args import ModelTraceArgs
from train.trace_trainer import TraceTrainer


class AbstractTraceJob(AbstractJob, ABC):

    def __init__(self, args: ModelTraceArgs):
        """
        Base job for task using a model (i.e. training, prediction, evaluation...)
        :param args: arguments used for configuring the model
        """
        super().__init__(args)
        self.trainer = TraceTrainer(args=self.args, model_generator=self.args.model_generator,
                                    dataset_creator=self.args.trace_dataset_creator)
