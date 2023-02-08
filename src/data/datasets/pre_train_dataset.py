import os
import shutil

from datasets import load_dataset
from torch.utils.data import Dataset

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
        tokenizer = model_manager.get_tokenizer()

        def tokenize_batches(examples):
            tokenized_example = tokenizer(examples["text"], truncation=True, max_length=self.block_size,
                                          return_special_tokens_mask=True, return_overflowing_tokens=True)
            return tokenized_example

        def tokenize_and_chunk(texts):
            all_input_ids = []
            for input_ids in tokenizer(texts["text"]["input_ids"]):
                all_input_ids.extend(input_ids)
                all_input_ids.append(tokenizer.eos_token)
            chunks = []
            for idx in range(0, len(all_input_ids, self.block_size)):
                chunks.append(all_input_ids[idx: idx + self.block_size])
            return {"input_ids": chunks}

        dataset = load_dataset("text", data_files={"train": self.training_file_path})
        dataset = dataset.map(tokenize_batches, batched=True)
        dataset = dataset.map(tokenize_and_chunk, batched=True)
        return dataset["train"]

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
