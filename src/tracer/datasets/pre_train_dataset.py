from torch.utils.data import Dataset
from transformers import LineByLineTextDataset

from tracer.datasets.abstract_dataset import AbstractDataset
from tracer.models.model_generator import ModelGenerator


class PreTrainDataset(AbstractDataset):

    def __init__(self, training_file_path: str, block_size: int, **kwargs):
        self.training_file_path = training_file_path
        self.block_size = block_size
        self.kwargs = kwargs

    def to_trainer_dataset(self, model_generator: ModelGenerator) -> Dataset:
        """
        Uses pretrain datafile to create a Dataset (i.e. LineByLineDataset) for Huggingface (HF) trainer.
        :param model_generator: The model generator determining tokenizer to be used.
        :return: A datasets used by the HF trainer.
        """
        return LineByLineTextDataset(tokenizer=model_generator.get_tokenizer(),
                                     file_path=self.training_file_path,
                                     block_size=self.block_size,
                                     **self.kwargs)
