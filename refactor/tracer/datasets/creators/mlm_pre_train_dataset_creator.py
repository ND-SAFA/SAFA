import os
import uuid
from os.path import dirname
from typing import List

from config.constants import BLOCK_SIZE_DEFAULT
from tracer.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.datasets.pre_train_dataset import PreTrainDataset
from tracer.pre_processing.steps.abstract_pre_processing_step import AbstractPreProcessingStep


class MLMPreTrainDatasetCreator(AbstractDatasetCreator):
    DELIMINATOR = "\n"
    OUTPUT_FILE_EXT = ".txt"

    def __init__(self, orig_data_path: str, training_data_dir: str = None,
                 pre_processing_steps: List[AbstractPreProcessingStep] = None,
                 block_size: int = BLOCK_SIZE_DEFAULT):
        """
        The masked learning model pretraining datasets creator
        :param orig_data_path: path to the original pretraining data
        :param training_data_dir: path to the directory to save the training datasets file (defaults to same as orig_data_path)
        :param pre_processing_steps: tuple containing the desired pre-processing steps and related params
        :param block_size: the block size for the LineByLineDataset
        """
        super().__init__(pre_processing_steps)
        self.orig_data_path = orig_data_path
        self.block_size = block_size
        self.id = str(uuid.uuid4())
        training_dataset_filename = self.id + self.OUTPUT_FILE_EXT
        training_data_dir = training_data_dir if training_data_dir else dirname(orig_data_path)
        self.training_dataset_file = os.path.join(training_data_dir, training_dataset_filename)

    def create(self) -> PreTrainDataset:
        """
        Creates the pretrain datasets
        :return: the datasets
        """
        files = self._get_file_list(self.orig_data_path)
        training_examples = self._read_data_files(files)
        dataset_file = self._write_training_examples(training_examples)
        return PreTrainDataset(dataset_file, block_size=self.block_size)

    @staticmethod
    def _get_file_list(data_path: str) -> List[str]:
        """
        Gets the list of files to use for the training
        :param data_path: path to the original pretraining
        :return: a list of files
        """
        if os.path.isfile(data_path):
            data_path, filename = os.path.split(data_path)
            files = [filename]
        elif os.path.isdir(data_path):
            files = os.listdir(data_path)
        else:
            raise Exception("Unable to read pretraining data file path " + data_path)
        return files

    def _read_data_files(self, files: List[str]) -> List[str]:
        """
        Reads the data files' content and pre-processes the text
        :param files: list of file names
        :return: a list of all files' content (training examples) split by new line
        """
        training_examples = []
        for file_name in files:
            if file_name[0] != ".":
                training_examples.extend(self._read_data_file(file_name))
        return training_examples

    def _read_data_file(self, file_name: str) -> List[str]:
        """
        Reads the data file content and pre-processes the text
        :param file_name: the name of the file
        :return: a list of file content (training examples) split by new line
        """
        with open(os.path.join(self.orig_data_path, file_name)) as data_file:
            file_content = data_file.read()
        return self._process_tokens(file_content.split(self.DELIMINATOR))

    def _write_training_examples(self, examples: List[str]) -> str:
        """
        Writes the training examples to the datasets file
        :param examples: a list of training examples
        :return: the path to the datasets file
        """
        training_file_content = self.DELIMINATOR.join(examples)
        os.makedirs(os.path.dirname(self.training_dataset_file), exist_ok=True)
        print("Exporting: ", self.training_dataset_file)
        with open(self.training_dataset_file, "w") as training_file:
            training_file.write(training_file_content)
        return self.training_dataset_file
