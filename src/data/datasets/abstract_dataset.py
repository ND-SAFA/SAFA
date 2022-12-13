from abc import abstractmethod
from typing import Any

from models.model_manager import ModelManager


class AbstractDataset:

    @abstractmethod
    def to_trainer_dataset(self, model_generator: ModelManager) -> Any:
        """
        Converts data to that used by Huggingface (HF) trainer.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data used by the HF trainer.
        """
        pass

    @abstractmethod
    def save(self, output_dir: str, filename: str) -> str:
        """
        Saves the dataset to the output dir
        :param output_dir: directory to save to
        :param filename: name of tthe file (no ext)
        :return: location the file was saved to
        """
        pass
