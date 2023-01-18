from abc import abstractmethod
from typing import Any

from models.model_manager import ModelManager
from util.base_object import BaseObject


class AbstractDataset(BaseObject):

    @abstractmethod
    def to_trainer_dataset(self, model_generator: ModelManager, batch_size_to_balance: int = None) -> Any:
        """
        Converts data to that used by Huggingface (HF) trainer.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :param batch_size_to_balance: The size of the batch. If provided, balances the batches with equal pos and neg links
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
