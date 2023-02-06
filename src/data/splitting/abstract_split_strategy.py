from abc import ABC, abstractmethod

from data.creators.abstract_dataset_creator import DatasetType


class AbstractSplitStrategy(ABC):
    """
    Representing a strategy for splitting a dataset.
    """

    @staticmethod
    @abstractmethod
    def create_split(dataset: DatasetType, percent_split: float, slice_num: int) -> DatasetType:
        """
        Creates the split of the dataset
        :param dataset: The dataset to split.
        :type percent_split: The percentage of the dataset contained in the second split.
        :type slice_num: The slice number to return.
        :return: TraceDatset containing slice of data.
        """
        raise NotImplementedError()
