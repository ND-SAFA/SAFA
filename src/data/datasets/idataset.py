from abc import abstractmethod
from typing import Any

from models.model_manager import ModelManager
from util.base_object import BaseObject


class iDataset(BaseObject):

    @abstractmethod
    def to_hf_dataset(self, model_generator: ModelManager) -> Any:
        """
        Converts data to a Huggingface (HF) Dataset.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data in a HF Dataset.
        """

    @abstractmethod
    def to_trainer_dataset(self, model_generator: ModelManager) -> Any:
        """
        Converts data to that used by Huggingface (HF) trainer.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data used by the HF trainer.
        """

    @abstractmethod
    def save(self, output_dir: str, filename: str) -> str:
        """
        Saves the dataset to the output dir
        :param output_dir: directory to save to
        :param filename: name of the file (no ext)
        :return: location the file was saved to
        """
