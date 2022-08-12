from abc import ABC

from common.jobs.abstract_job import AbstractJob
from common.jobs.abstract_arg_builder import AbstractArgBuilder
from pretrain.train.pretrainer import PreTrainer


class AbstractPreTrainJob(AbstractJob, ABC):

    def __init__(self, args_builder: AbstractArgBuilder):
        """
        Abstract job for pre-training
        :param args_builder: arguments used for pre-training
        """
        super().__init__(args_builder)
        self.pretrainer = PreTrainer(self.args)
