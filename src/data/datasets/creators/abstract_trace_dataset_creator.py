from abc import ABC, abstractmethod

from data.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner


class AbstractTraceDatasetCreator(AbstractDatasetCreator, ABC):

    def __init__(self, data_cleaner: DataCleaner):
        """
        Responsible for creating data in format for defined models.
        :param data_cleaner: Processes the artifact tokens.
        """
        super().__init__(data_cleaner)

    @abstractmethod
    def create(self) -> TraceDataset:
        """
        Creates the trace data
        :return: the data
        """
