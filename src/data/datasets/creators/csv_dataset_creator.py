from typing import Dict

from data.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.creators.readers.entity.csv_project_reader import CSVEntityReader
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner
from data.tree.trace_link import TraceLink


class CSVDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, data_file_path: str, data_cleaner: DataCleaner = None):
        """
        Constructs data in CSV format
        :param data_file_path: path to csv
        :param data_cleaner: Responsible for processing artifact tokens.
        """
        super().__init__(data_cleaner, use_linked_targets_only=False)
        self.data_file_path = data_file_path

    def create(self) -> TraceDataset:
        """
        Creates the data
        :return: the data
        """
        project_reader = CSVEntityReader(self.data_file_path)
        trace_links: Dict[int, TraceLink] = project_reader.get_entities()
        return TraceDataset(links=trace_links)
