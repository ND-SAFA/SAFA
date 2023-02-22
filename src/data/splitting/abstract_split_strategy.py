from abc import ABC, abstractmethod
from typing import List, Tuple, TypeVar

from sklearn.model_selection import train_test_split

from data.creators.abstract_dataset_creator import DatasetType
from util.random_util import RandomUtil

GenericDatum = TypeVar("GenericData")
GenericData = List[GenericDatum]


class AbstractSplitStrategy(ABC):
    """
    Representing a strategy for splitting a dataset.
    """

    def __init__(self, split_percentage: float):
        """
        Initializes strategy with given split percentage
        :param split_percentage: The percent of the data to use for this split
        """
        self.total_split_percentage = split_percentage
        self.percent_of_split_dataset = split_percentage

    def update_percent_of_split_dataset(self, percent_of_split_dataset: float) -> None:
        """
        Updates the percent of the
        :param percent_of_split_dataset:
        :return:
        """
        self.percent_of_split_dataset = percent_of_split_dataset

    @abstractmethod
    def create_split(self, dataset: DatasetType) -> Tuple[DatasetType, DatasetType]:
        """
        Creates the split of the dataset
        :param dataset: The dataset to split.
        :return: Dataset containing slice of data.
        """
        raise NotImplementedError()

    @staticmethod
    def split_data(data: GenericData, first_split_percent: float, labels: List[int] = None, **kwargs) -> Tuple[GenericData, GenericData]:
        """
        Splits data into slices using labels to guarantee equal proportions of the labels in each split
        :param data: The data to split.
        :param first_split_percent: The percentage of the data to be contained in second split
        :param labels: The labels to stratify data with.
        :return: Two slices of data.
        """
        random_state = RandomUtil.CURRENT_SEED if RandomUtil.CURRENT_SEED is not None else 0
        return train_test_split(data, test_size=1 - first_split_percent, stratify=labels, random_state=random_state, **kwargs)
