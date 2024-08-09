from abc import ABC, abstractmethod
from typing import List, Tuple, Type, TypeVar

from sklearn.model_selection import train_test_split

from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.override import overrides
from common_resources.tools.util.random_util import RandomUtil
from common_resources.data.creators.abstract_dataset_creator import DatasetType

GenericDatum = TypeVar("GenericData")
GenericData = List[GenericDatum]


class AbstractSplitStrategy(ABC):
    """
    Representing a strategy for splitting a dataset.
    """

    @staticmethod
    @abstractmethod
    def create_split(dataset: DatasetType, second_split_percentage: float) -> Tuple[DatasetType, DatasetType]:
        """
        Creates the split of the dataset
        :param dataset: The dataset to split.
        :param second_split_percentage: The percentage of the data to be contained in second split
        :return: Dataset containing slice of data.
        """
        raise NotImplementedError()

    @staticmethod
    def split_data(data: GenericData, second_split_percentage: float, labels: List[int] = None, **kwargs) \
            -> Tuple[GenericData, GenericData]:
        """
        Splits data into slices using labels to guarantee equal proportions of the labels in each split
        :param data: The data to split.
        :param second_split_percentage: The percentage of the data to be contained in second split
        :param labels: The labels to stratify data with.
        :return: Two slices of data.
        """
        random_state = RandomUtil.CURRENT_SEED if RandomUtil.CURRENT_SEED is not None else 0
        return train_test_split(data, test_size=second_split_percentage, stratify=labels, random_state=random_state, **kwargs)

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from common_resources.data.splitting.supported_split_strategy import SupportedSplitStrategy
        return SupportedSplitStrategy
