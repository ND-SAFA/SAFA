from typing import Type

from constants import REMOVE_ORPHANS_DEFAULT
from data.creators.abstract_dataset_creator import AbstractDatasetCreator, DatasetType
from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.processing.cleaning.data_cleaner import DataCleaner
from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.supported_dataset_reader import SupportedDatasetReader
from util.base_object import BaseObject
from util.override import overrides


class MultiTraceDatasetCreator(AbstractDatasetCreator):
    """
    Responsible for creating Combining Multiple TraceDataset from DataFrames containing artifacts, traces, and
    layer mappings.
    """
    DELIMITER = "-"

    def __init__(self, project_readers: [AbstractProjectReader], data_cleaner: DataCleaner = None,
                 remove_orphans: bool = REMOVE_ORPHANS_DEFAULT):
        """
        Initializes creator with entities extracted from reader.
        :param project_readers: The project readers responsible for extracting project entities for each dataset.
        :param data_cleaner: Data Cleaner containing list of data cleaning steps to perform on artifact tokens.
        :param remove_orphans: Whether to remove artifacts without a positive trace link.
        """
        super().__init__(data_cleaner)
        self.project_readers = project_readers
        self.remove_orphans = remove_orphans

    def create(self) -> DatasetType:
        """
        Creates TraceDataset from each project reader and combines.
        :return: TraceDataset.
        """
        multi_dataset = None
        for reader in self.project_readers:
            dataset = TraceDatasetCreator(project_reader=reader, data_cleaner=self.data_cleaner,
                                          remove_orphans=self.remove_orphans).create()
            if multi_dataset is None:
                multi_dataset = dataset
            else:
                multi_dataset += dataset  # combine datasets
        return multi_dataset

    def get_name(self) -> str:
        """
        :return: Returns name of combination of datasets.
        """
        return self.DELIMITER.join([p.get_project_name() for p in self.project_readers])

    @classmethod
    @overrides(BaseObject)
    def _get_child_enum_class(cls, abstract_class: Type, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        return SupportedDatasetReader
