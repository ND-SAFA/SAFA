from abc import abstractmethod

from data.datasets.dataset_role import DatasetRole
from train.trace_output.trace_prediction_output import TracePredictionOutput
from train.trace_output.trace_train_output import TraceTrainOutput


class iTrainer:

    @abstractmethod
    def perform_training(self, checkpoint: str = None) -> TraceTrainOutput:
        """
        Handles training of the model
        :param checkpoint: If provided, will resume training from given checkpoint
        :return: The training output
        """

    @abstractmethod
    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :return: THe prediction output
        """