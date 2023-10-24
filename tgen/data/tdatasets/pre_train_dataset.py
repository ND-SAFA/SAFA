from typing import Any

import pandas as pd
from datasets import load_dataset
from torch.utils.data import Dataset
from transformers import PreTrainedTokenizer

from tgen.data.tdatasets.idataset import iDataset
from tgen.models.model_manager import ModelManager


class PreTrainDataset(iDataset):

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

    def to_hf_dataset(self, model_generator: ModelManager) -> Any:
        """
        Converts data to a Huggingface (HF) Dataset.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data in a HF Dataset.
        """
        return self.to_trainer_dataset(model_generator)

    def to_trainer_dataset(self, model_manager: ModelManager) -> Dataset:
        """
        Uses pretrain datafile to create a Dataset (i.e. LineByLineDataset) for Huggingface (HF) trainer.
        :param model_manager: The model generator determining tokenizer to be used.
        :return: A data used by the HF trainer.
        """
        tokenizer = model_manager.get_tokenizer()
        input_ids = self.create_input_ids(tokenizer, tex)
        dataset = load_dataset("text", data_files={"train": self.training_file_path})
        dataset = dataset.map(create_input_ids, batched=True, remove_columns=["text"], desc="Tokenizing dataset")
        return dataset["train"]

    def as_creator(self, project_path: str):
        """
        Pre train dataset cannot be converted to creator
        """
        raise NotImplementedError("Pre train dataset cannot be converted to creator")

    @staticmethod
    def create_input_ids(tokenizer: PreTrainedTokenizer, texts: pd.DataFrame, block_size: int):
        """

        :param texts:
        :return:
        """
        all_input_ids = []
        tokenizer_output = tokenizer(texts["text"], add_special_tokens=True)["input_ids"]
        for input_ids in tokenizer_output:
            all_input_ids.extend(input_ids)
            all_input_ids.append(tokenizer.sep_token_id)
        chunks = []
        for idx in range(0, len(all_input_ids), block_size):
            chunks.append(all_input_ids[idx: idx + block_size])
        return {"input_ids": chunks}
