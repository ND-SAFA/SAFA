from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from data.datasets.abstract_dataset import AbstractDataset
from data.processing.cleaning.data_cleaner import DataCleaner
from util.base_object import BaseObject

DatasetType = TypeVar("DatasetType", bound=AbstractDataset)


class AbstractDatasetCreator(BaseObject, ABC, Generic[DatasetType]):

    def __init__(self, data_cleaner: DataCleaner = None):
        """
        Responsible for creating data in format for defined models.
        :param data_cleaner: the data cleaner to use on the data
        """
        self.data_cleaner = DataCleaner([]) if data_cleaner is None else data_cleaner

    @abstractmethod
    def create(self) -> DatasetType:
        """
        Creates the data
        :return: the data
        """
