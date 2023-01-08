from abc import ABC, abstractmethod
from typing import Sized, List

from data.datasets.trace_dataset import TraceDataset


class AbstractSplitStrategy(ABC):
    """
    Representing a strategy for splitting a dataset.
    """

    @staticmethod
    @abstractmethod
    def create_split(trace_dataset: TraceDataset, percent_split: float, slice_num: int):
        """
        Creates the split of the dataset
        :param trace_dataset: The dataset to split.
        :type percent_split: The percentage of the dataset contained in the second split.
        :type slice_num: The slice number to return.
        :return: TraceDatset containing slice of data.
        """
        raise NotImplementedError()

    @staticmethod
    def get_first_split_size(data: Sized, percent_split: float) -> int:
        """
        Gets the size of the data for the first split
        :param data: a list of the data
        :param percent_split: The percentage of samples in second split.
        :return: the size of the data split
        """
        return len(data) - round(len(data) * percent_split)

    @staticmethod
    def get_data_split(data: List, percent_split: float = None, for_second_split: bool = False, split_size: int = None) -> List:
        """
        Splits the data and returns the split
        :param data: a list of the data
        :param percent_split: The percentage of samples in second split.
        :param for_second_split: If True, returns the second portion.
        :param split_size: May be specified instead of percent split to get a certain number of links
        :return: the subsection of the data in the split
        """
        assert(percent_split is not None or split_size is not None)
        split_size = AbstractSplitStrategy.get_first_split_size(data, percent_split) if split_size is None else split_size
        return data[split_size:] if for_second_split else data[:split_size]
