from abc import ABC, abstractmethod

from data.datasets.trace_dataset import TraceDataset


class AbstractSplitStrategy(ABC):
    """
    Representing a strategy for splitting a dataset.
    """

    @staticmethod
    @abstractmethod
    def create_split(trace_dataset: TraceDataset, percent_split: float, slice_num: int) -> TraceDataset:
        """
        Creates the split of the dataset
        :param trace_dataset: The dataset to split.
        :type percent_split: The percentage of the dataset contained in the second split.
        :type slice_num: The slice number to return.
        :return: TraceDatset containing slice of data.
        """
        raise NotImplementedError()
