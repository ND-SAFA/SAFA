from abc import abstractmethod
from dataclasses import dataclass
from typing import Type, Union

from common_resources.data.tdatasets.dataset_role import DatasetRole
from common_resources.data.tdatasets.idataset import iDataset
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset

from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.override import overrides
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trace_output.trace_train_output import TraceTrainOutput
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager


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

    @staticmethod
    def convert_dataset_to_prompt_dataset(dataset: Union[PromptDataset, TraceDataset]) -> PromptDataset:
        """
        If the dataset is not a prompt dataset, it is converted to one
        :param dataset: The original dataset
        :return: The dataset a prompt dataset
        """
        if not isinstance(dataset, PromptDataset):
            dataset = PromptDataset(trace_dataset=dataset)
        return dataset

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
