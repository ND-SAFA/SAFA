from abc import ABC, abstractmethod
from typing import List, Union

from tracer.dataset.abstract_dataset import AbstractDataset
from tracer.pre_processing.pre_processor import PreProcessor


class AbstractDatasetCreator(ABC):

    def __init__(self, pre_processor: PreProcessor):
        """
        Responsible for creating dataset in format for defined models.
        :pre_processor: the pre_processor to run on the data
        """
        self.pre_processor = pre_processor

    @abstractmethod
    def create(self) -> AbstractDataset:
        """
        Creates the dataset
        :return: the dataset
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

        tokens = self.pre_processor.run(tokens=tokens)

        if len(tokens) == 1:
            tokens = tokens.pop()

        return tokens
