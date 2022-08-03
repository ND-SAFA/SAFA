from abc import ABC

from jobs.abstract.abstract_job import AbstractJob
from jobs.pretrain.model_pretrain_args import ModelPretrainArgs
from pretrain.pretrainer import PreTrainer


class AbstractPreTrainJob(AbstractJob, ABC):

    def __init__(self, args: ModelPretrainArgs):
        """
        Abstract job for pre-training
        :param args: arguments used for pre-training
        """
        super().__init__(args)
        self.pretrain = PreTrainer(args)
