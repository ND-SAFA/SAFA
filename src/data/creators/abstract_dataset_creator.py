from abc import ABC, abstractmethod
from typing import List, Union

from data.datasets.pre_train_dataset import PreTrainDataset
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner


class AbstractDatasetCreator(ABC):

    def __init__(self, data_cleaner: DataCleaner = None):
        """
        Responsible for creating data in format for defined models.
        :param data_cleaner: the data cleaner to use on the data
        """
        self.data_cleaner = data_cleaner

    @abstractmethod
    def create(self) -> Union[TraceDataset, PreTrainDataset]:
        """
        Creates the data
        :return: the data
        """
        pass

    def _process_tokens(self, tokens: Union[List[str], str]) -> Union[List[str], str]:
        """
        Processes the artifact tokens using the given pre-processor
        :param tokens: artifact content or a list of artifact content strings
        :return: the processed content
        """
        if not isinstance(tokens, list):
            tokens = [tokens]

        tokens = self.data_cleaner.run(tokens=tokens) if self.data_cleaner else tokens

        if len(tokens) == 1:
            tokens = tokens.pop()

        return tokens
