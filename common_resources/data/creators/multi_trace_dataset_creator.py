from typing import List

from common_resources.tools.constants.dataset_constants import REMOVE_ORPHANS_DEFAULT
from common_resources.data.creators.abstract_dataset_creator import AbstractDatasetCreator, DatasetType
from common_resources.data.creators.trace_dataset_creator import TraceDatasetCreator
from common_resources.data.processing.cleaning.data_cleaner import DataCleaner
from common_resources.data.readers.abstract_project_reader import AbstractProjectReader


class MultiTraceDatasetCreator(AbstractDatasetCreator):
    """
    Responsible for creating Combining Multiple TraceDataset from DataFrames containing artifacts, traces, and
    layer mappings.
    """
    DELIMITER = "-"

    def __init__(self, project_readers: List[AbstractProjectReader], data_cleaner: DataCleaner = None,
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
