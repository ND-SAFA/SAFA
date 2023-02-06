from abc import ABC, abstractmethod
from typing import List, Tuple, TypeVar

from sklearn.model_selection import train_test_split

from data.creators.abstract_dataset_creator import DatasetType

GenericDatum = TypeVar("GenericData")
GenericData = List[GenericDatum]


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
        :return: Dataset containing slice of data.
        """
        raise NotImplementedError()

    @staticmethod
    def split_data(data: GenericData, percent_split: float, labels: List[int] = None, **kwargs) -> Tuple[GenericData, GenericData]:
        """
        Splits data into slices using labels to guarantee equal proportions of the labels in each split
        :param data: The data to split.
        :param percent_split: The percentage of the data to be contained in second split
        :param labels: The labels to stratify data with.
        :return: Two slices of data.
        """
        return train_test_split(data, test_size=percent_split, stratify=labels, random_state=0, **kwargs)
