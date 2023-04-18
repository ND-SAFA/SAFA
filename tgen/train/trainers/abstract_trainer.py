from abc import abstractmethod

from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.train.trace_output.trace_train_output import TraceTrainOutput
from tgen.util.base_object import BaseObject


class AbstractTrainer(BaseObject):

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager):
        """
        Initializes the trainer with a dataset manager used for training and predictions
        :param trainer_dataset_manager: The dataset manager used for training and predictions
        """
        self.trainer_dataset_manager = trainer_dataset_manager

    @abstractmethod
    def perform_training(self) -> TraceTrainOutput:
        """
        Handles training of the model
        :return: The training output
        """

    @abstractmethod
    def perform_prediction(self, dataset_role: DatasetRole = DatasetRole.EVAL, dataset: iDataset = None) -> TracePredictionOutput:
        """
        Performs the prediction and (optionally) evaluation for the model
        :param dataset_role: The dataset role to use for evaluation (e.g. VAL or EVAL)
        :param dataset: The dataset to use instead of from the dataset manager
        :return: THe prediction output
        """

    @abstractmethod
    def cleanup(self) -> None:
        """
        performs any necessary cleanup at the end of the job
        :return: None
        """
