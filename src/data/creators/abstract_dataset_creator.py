from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from data.datasets.idataset import iDataset
from data.processing.cleaning.data_cleaner import DataCleaner
from util.base_object import BaseObject

DatasetType = TypeVar("DatasetType", bound=iDataset)


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

    @abstractmethod
    def get_name(self) -> str:
        """
        :return: Returns the name of the dataset.
        """
