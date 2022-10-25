import os
import uuid
from typing import List, Dict

from config.constants import BLOCK_SIZE_DEFAULT
from tracer.dataset.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.dataset.pre_train_dataset import PreTrainDataset
from tracer.pre_processing.pre_processor import PreProcessor


class MLMPreTrainDatasetCreator(AbstractDatasetCreator):
    DELIMINATOR = "\n"
    OUTPUT_FILE_EXT = ".txt"

    def __init__(self, orig_data_path: str, training_data_dir: str, pre_processor: PreProcessor = None,
                 block_size: int = BLOCK_SIZE_DEFAULT):
        """
        The masked learning model pretraining dataset creator
        :param orig_data_path: path to the original pretraining
        :param training_data_dir: path to the directory to save the training dataset file
        :param pre_processor: the pre_processor to run on the data
        :param block_size: the block size for the LineByLineDataset
        """
        super().__init__(pre_processor)
        self.orig_data_path = orig_data_path
        self.block_size = block_size
        self.id = str(uuid.uuid4())
        training_dataset_filename = self.id + self.OUTPUT_FILE_EXT
        self.training_dataset_file = os.path.join(training_data_dir, training_dataset_filename)

    def create(self) -> PreTrainDataset:
        dataset_file = self._create_training_datafile(self.orig_data_path)
        return PreTrainDataset(dataset_file, block_size=self.block_size)

    def _create_training_datafile(self, data_path: str) -> str:
        """
        Reads text files in given data_path and returns a temporary file containing collection.
        :param data_path: Path to txt file or folder containing txt files.
        :return: Path to temporary file containing formatted training examples.
        """

        if os.path.isfile(data_path):
            data_path, filename = os.path.split(data_path)
            files = [filename]
        elif os.path.isdir(data_path):
            files = os.listdir(data_path)
        else:
            raise Exception("Unable to read pretraining data file path " + data_path)

        training_examples = self._read_data_files(data_path, files)

        return self._write_training_examples(training_examples)

    def _read_data_files(self, data_path: str, files: List[str]) -> List[str]:
        """
        Reads the data files' content and pre-processes the text
        :param data_path: the path to the data files
        :param files: list of file names
        :return: a list of all files' content (training examples) split by new line
        """
        training_examples = []
        for file_name in files:
            if file_name[0] == ".":
                continue
            file_path = os.path.join(data_path, file_name)
            training_examples.extend(self._read_data_file(file_path))
        return training_examples

    def _read_data_file(self, file_path: str) -> List[str]:
        """
        Reads the data file content and pre-processes the text
        :param file_path: the path to the file
        :return: a list of file content (training examples) split by new line
        """
        with open(file_path) as data_file:
            file_content = data_file.read()
        return self._process_tokens(file_content.split(self.DELIMINATOR))

    def _write_training_examples(self, examples: List[str]) -> str:
        """
        Writes the training examples to the dataset file
        :param examples: a list of training examples
        :return: the path to the dataset file
        """
        training_file_content = self.DELIMINATOR.join(examples)
        os.makedirs(os.path.dirname(self.training_dataset_file), exist_ok=True)
        print("Exporting: ", self.training_dataset_file)
        with open(self.training_dataset_file, "w") as training_file:
            training_file.write(training_file_content)
        return self.training_dataset_file
