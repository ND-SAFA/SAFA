import os
import shutil

from torch.utils.data import Dataset
from transformers import LineByLineTextDataset

from data.datasets.abstract_dataset import AbstractDataset
from models.model_manager import ModelManager


class PreTrainDataset(AbstractDataset):

    def __init__(self, training_file_path: str, block_size: int, **kwargs):
        """
        Represents a pretraining dataset
        :param training_file_path: the path to the file containing training examples
        :param block_size: the size to split the concatenated text into smaller chunks
        :param kwargs: any additional parameters used in the dataset
        """
        self.training_file_path = training_file_path
        self.block_size = block_size
        self.kwargs = kwargs

    def to_trainer_dataset(self, model_manager: ModelManager) -> Dataset:
        """
        Uses pretrain datafile to create a Dataset (i.e. LineByLineDataset) for Huggingface (HF) trainer.
        :param model_manager: The model generator determining tokenizer to be used.
        :return: A data used by the HF trainer.
        """
        return LineByLineTextDataset(tokenizer=model_manager.get_tokenizer(),
                                     file_path=self.training_file_path,
                                     block_size=self.block_size,
                                     **self.kwargs)

    def save(self, output_dir: str, filename: str) -> str:
        """
        Saves the dataset to the output dir
        :param output_dir: directory to save to
        :param filename: name of the file (no ext)
        :return: location the file was saved to
        """
        filepath = os.path.join(output_dir, filename)
        shutil.copy(self.training_file_path, filepath)
        return filepath
