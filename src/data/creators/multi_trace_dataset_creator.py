from typing import Generic

from data.creators.abstract_dataset_creator import AbstractDatasetCreator, DatasetType
from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.processing.cleaning.data_cleaner import DataCleaner
from data.readers.abstract_project_reader import AbstractProjectReader


class MultiTraceDatasetCreator(AbstractDatasetCreator[Generic[DatasetType]]):
    """
    Responsible for creating Combining Multiple TraceDataset from DataFrames containing artifacts, traces, and
    layer mappings.
    """

    def __init__(self, project_readers: [AbstractProjectReader], data_cleaner: DataCleaner = None,
                 filter_unlinked_artifacts: bool = False):
        """
        Initializes creator with entities extracted from reader.
        :param project_readers: The project readers responsible for extracting project entities for each dataset.
        :param data_cleaner: Data Cleaner containing list of data cleaning steps to perform on artifact tokens.
        :param filter_unlinked_artifacts: Whether to remove artifacts without a positive trace link.
        """
        super().__init__(data_cleaner)
        self.project_readers = project_readers
        self.should_filter_unlinked_artifacts = filter_unlinked_artifacts

    def create(self) -> DatasetType:
        """
        Creates TraceDataset from each project reader and combines.
        :return: TraceDataset.
        """
        multi_dataset = None
        for reader in self.project_readers:
            dataset = TraceDatasetCreator(project_reader=reader, data_cleaner=self.data_cleaner,
                                          filter_unlinked_artifacts=self.should_filter_unlinked_artifacts).create()
            if multi_dataset is None:
                multi_dataset = dataset
            else:
                multi_dataset += dataset  # combine datasets
        return multi_dataset
