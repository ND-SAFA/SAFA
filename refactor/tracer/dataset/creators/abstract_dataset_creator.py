from abc import ABC, abstractmethod

from tracer.dataset.trace_dataset import TraceDataset
from tracer.pre_processing.pre_processor import PreProcessor


class AbstractDatasetCreator(ABC):

    def __init__(self, pre_processor: PreProcessor = None):
        """
        Responsible for creating dataset in format for defined models.
        :pre_processor: the pre_processor to run on the data
        """
        self.pre_processor = pre_processor

    @abstractmethod
    def create(self) -> TraceDataset:
        """
        Gets the dataset
        :return: the dataset
        """
        pass
