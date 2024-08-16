import os
import uuid
from os.path import dirname
from typing import List

from gen_common.constants import BLOCK_SIZE_DEFAULT, NEW_LINE
from gen_common.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from gen_common.data.processing.cleaning.data_cleaner import DataCleaner
from gen_common.data.readers.pre_train_project_reader import PreTrainProjectReader
from gen_common.data.tdatasets.pre_train_dataset import PreTrainDataset
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util import FileUtil


class MLMPreTrainDatasetCreator(AbstractDatasetCreator[PreTrainDataset]):
    DELIMINATOR = NEW_LINE
    OUTPUT_FILE_EXT = ".txt"

    def __init__(self, orig_data_path: str, training_data_dir: str = None,
                 data_cleaner: DataCleaner = None,
                 block_size: int = BLOCK_SIZE_DEFAULT):
        """
        The masked learning model pretraining data creator
        :param orig_data_path: path to the original pretraining data
        :param training_data_dir: path to the directory to save the training data file (defaults to same as orig_data_path)
        :param data_cleaner: the cleaner responsible for processing artifact tokens.
        :param block_size: the block size for the LineByLineDataset
        """
        super().__init__(data_cleaner)
        self.orig_data_path = orig_data_path
        self.block_size = block_size
        self.id = str(uuid.uuid4())
        training_dataset_filename = self.id + self.OUTPUT_FILE_EXT
        training_data_dir = training_data_dir if training_data_dir else dirname(orig_data_path)
        self.training_dataset_file = os.path.join(training_data_dir, training_dataset_filename)

    def create(self) -> PreTrainDataset:
        """
        Reads pre-training documents and converts lines into pre-training examples.
        :return: The pre-training dataset.
        """
        pre_train_reader = PreTrainProjectReader(self.orig_data_path)
        training_examples = pre_train_reader.read_project()
        dataset_file = self._write_training_examples(training_examples)
        return PreTrainDataset(dataset_file, block_size=self.block_size)

    def get_name(self) -> str:
        """
        :return: Returns the file name of the data path.
        """
        return FileUtil.get_file_name(self.orig_data_path)

    def _write_training_examples(self, examples: List[str]) -> str:
        """
        Writes the training examples to the data file
        :param examples: a list of training examples
        :return: the path to the data file
        """
        training_file_content = self.DELIMINATOR.join(examples)
        os.makedirs(os.path.dirname(self.training_dataset_file), exist_ok=True)
        logger.info(f"Exporting: {self.training_dataset_file}")
        with open(self.training_dataset_file, "w") as training_file:
            training_file.write(training_file_content)
        return self.training_dataset_file
