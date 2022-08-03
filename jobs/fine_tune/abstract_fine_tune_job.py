from abc import ABC

from jobs.abstract.abstract_job import AbstractJob
from jobs.fine_tune.model_fine_tune_args import ModelFineTuneArgs
from train.model_trainer import ModelTrainer


class AbstractFineTuneJob(AbstractJob, ABC):

    def __init__(self, args: ModelFineTuneArgs):
        """
        Base job for task using a model (i.e. training, prediction, evaluation...)
        :param args: arguments used for configuring the model
        """
        super().__init__(args)
        self.trainer = ModelTrainer(args=self.args, model_generator=self.args.model_generator,
                                    dataset_creator=self.args.dataset)
