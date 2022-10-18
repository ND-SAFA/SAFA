from abc import ABC, abstractmethod

from tracer.dataset.trace_dataset import TraceDataset


class AbstractDatasetCreator(ABC):
    """
    Responsible for creating dataset in format for defined models.
    """

    @abstractmethod
    def create(self) -> TraceDataset:
        """
        Gets the dataset
        :return: the dataset
        """
        pass
