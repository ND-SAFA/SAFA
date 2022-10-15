from abc import ABC, abstractmethod

from dataset.trace_dataset import TraceDataset


class AbstractDatasetCreator(ABC):
    """
    Responsible for creating dataset in format for defined models.
    """

    @abstractmethod
    def get_dataset(self) -> TraceDataset:
        """
        Gets the dataset
        :return: the dataset
        """
        pass
