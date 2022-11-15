from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Union

from tracer.datasets.abstract_dataset import AbstractDataset
from tracer.pre_processing.pre_processing_option import PreProcessingOption
from tracer.pre_processing.pre_processor import PreProcessor


class AbstractDatasetCreator(ABC):

    def __init__(self, pre_processing_params: Tuple[List[PreProcessingOption], Dict]):
        """
        Responsible for creating datasets in format for defined models.
        :param pre_processing_params: tuple containing the desired pre-processing steps and related params
        """
        self.pre_processor = self._make_pre_processor(pre_processing_params)

    @abstractmethod
    def create(self) -> AbstractDataset:
        """
        Creates the datasets
        :return: the datasets
        """
        pass

    @staticmethod
    def _make_pre_processor(pre_processing_params: Tuple[List[PreProcessingOption], Dict] = None) -> PreProcessor:
        """
        Handles making the pre_processor
        :param pre_processing_params: tuple containing the desired pre-processing steps and related params
        :return: the pre_processor
        """
        if pre_processing_params:
            pre_processor_options, pre_processor_params = pre_processing_params
            return PreProcessor(pre_processor_options, **pre_processor_params)
        return PreProcessor()

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
