from abc import abstractmethod
from typing import Any

from tgen.common.util.base_object import BaseObject
from tgen.models.model_manager import ModelManager


class iDataset(BaseObject):

    @abstractmethod
    def to_hf_dataset(self, model_generator: ModelManager) -> Any:
        """
        Converts data to a Huggingface (HF) Dataset.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data in a HF Dataset.
        """

    @abstractmethod
    def to_trainer_dataset(self, **kwargs) -> Any:
        """
        Converts data to that used by Huggingface (HF) trainer.
        :param kwargs: The arguments needed to create the trainer dataset
        :return: A data used by the HF trainer.
        """

    @abstractmethod
    def as_creator(self, project_path: str):
        """
        Converts the dataset into a creator that can remake it
        :param project_path: The path to save the dataset at for reloading
        :return: The dataset creator
        """

    def to_yaml(self, export_path: str):
        """
        Creates a yaml savable dataset by saving as a creator.
        :param export_path: The path to export everything to
        :return: The dataset as a creator
        """
        return self.as_creator(export_path)
