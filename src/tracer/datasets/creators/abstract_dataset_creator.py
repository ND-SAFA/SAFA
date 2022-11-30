from abc import ABC, abstractmethod
from typing import List, Union

from tracer.datasets.pre_train_dataset import PreTrainDataset
from tracer.datasets.trace_dataset import TraceDataset
from tracer.pre_processing.pre_processor import PreProcessor
from tracer.pre_processing.steps.abstract_pre_processing_step import AbstractPreProcessingStep


class AbstractDatasetCreator(ABC):

    def __init__(self, pre_processing_steps: List[AbstractPreProcessingStep]):
        """
        Responsible for creating datasets in format for defined models.
        :param pre_processing_steps: List of pre-processing steps for dataset.
        """
        self._pre_processor = self._make_pre_processor(pre_processing_steps)

    @abstractmethod
    def create(self) -> Union[TraceDataset, PreTrainDataset]:
        """
        Creates the datasets
        :return: the datasets
        """
        pass

    @staticmethod
    def _make_pre_processor(pre_processing_steps: List[AbstractPreProcessingStep] = None) -> PreProcessor:
        """
        Handles making the pre_processor
        :param pre_processing_steps: tuple containing the desired pre-processing steps and related params
        :return: the pre_processor
        """
        if pre_processing_steps:
            return PreProcessor(pre_processing_steps)
        return PreProcessor([])

    def _process_tokens(self, tokens: Union[List[str], str]) -> Union[List[str], str]:
        """
        Processes the artifact tokens using the given pre-processor
        :param tokens: artifact content or a list of artifact content strings
        :return: the processed content
        """
        if not isinstance(tokens, list):
            tokens = [tokens]

        tokens = self._pre_processor.run(tokens=tokens)

        if len(tokens) == 1:
            tokens = tokens.pop()

        return tokens
