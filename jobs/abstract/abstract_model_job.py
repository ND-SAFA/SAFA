from abc import ABC

from jobs.abstract.abstract_job import AbstractJob
from jobs.train.model_training_args import ModelTrainingArgs
from train.model_trainer import ModelTrainer


class AbstractModelJob(AbstractJob, ABC):

    def __init__(self, args: ModelTrainingArgs):
        """
        Base job for task using a model (i.e. training, prediction, evaluation...)
        :param args: arguments used for configuring the model
        """
        super().__init__(args)
        self.trainer = ModelTrainer(args=self.args, model_generator=self.args.model_generator,
                                    dataset_creator=self.args.dataset)
