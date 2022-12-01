from abc import ABC, abstractmethod
from typing import List, Union

from tracer.datasets.pre_train_dataset import PreTrainDataset
from tracer.datasets.trace_dataset import TraceDataset
from tracer.datasets.processing.cleaning.data_cleaner import DataCleaner
from tracer.datasets.processing.abstract_data_processing_step import AbstractDataProcessingStep


class AbstractDatasetCreator(ABC):

    def __init__(self, data_cleaning_steps: List[AbstractDataProcessingStep]):
        """
        Responsible for creating datasets in format for defined models.
        :param data_cleaning_steps: List of pre-processing steps for dataset.
        """
        self._data_cleaner = self._make_data_cleaner(data_cleaning_steps)

    @abstractmethod
    def create(self) -> Union[TraceDataset, PreTrainDataset]:
        """
        Creates the datasets
        :return: the datasets
        """
        pass

    @staticmethod
    def _make_data_cleaner(data_cleaning_steps: List[AbstractDataProcessingStep] = None) -> DataCleaner:
        """
        Handles making the pre_processor
        :param data_cleaning_steps: tuple containing the desired pre-processing steps and related params
        :return: the pre_processor
        """
        if data_cleaning_steps:
            return DataCleaner(data_cleaning_steps)
        return DataCleaner([])

    def _process_tokens(self, tokens: Union[List[str], str]) -> Union[List[str], str]:
        """
        Processes the artifact tokens using the given pre-processor
        :param tokens: artifact content or a list of artifact content strings
        :return: the processed content
        """
        if not isinstance(tokens, list):
            tokens = [tokens]

        tokens = self._data_cleaner.run(tokens=tokens)

        if len(tokens) == 1:
            tokens = tokens.pop()

        return tokens
