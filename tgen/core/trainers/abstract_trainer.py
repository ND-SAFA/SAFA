from abc import abstractmethod
from dataclasses import dataclass
from typing import Type

from tgen.common.util.base_object import BaseObject
from tgen.common.util.override import overrides
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trace_output.trace_train_output import TraceTrainOutput
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.idataset import iDataset


class AbstractTrainer(BaseObject):

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, trainer_args: dataclass):
        """
        Initializes the trainer with a dataset manager used for training and predictions
        :param trainer_dataset_manager: The dataset manager used for training and predictions
        :param trainer_args: The arguments to the trainer.
        """
        self.trainer_dataset_manager = trainer_dataset_manager
        self.trainer_args = trainer_args

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

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from tgen.core.trainers.supported_trainer import SupportedTrainer
        return SupportedTrainer
