from typing import Dict, List

from data.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.creators.readers.entity.csv_project_reader import CSVProjectReader
from data.datasets.trace_dataset import TraceDataset
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from data.tree.trace_link import TraceLink


class CSVDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, data_file_path: str, data_cleaning_steps: List[AbstractDataProcessingStep] = None):
        """
        Constructs data in CSV format
        :param data_file_path: path to csv
        :param data_cleaning_steps: tuple containing the desired pre-processing steps and related params
        """
        super().__init__(data_cleaning_steps, use_linked_targets_only=False)
        self.data_file_path = data_file_path

    def create(self) -> TraceDataset:
        """
        Creates the data
        :return: the data
        """
        project_reader = CSVProjectReader(self.data_file_path)
        trace_links: Dict[int, TraceLink] = project_reader.get_entities()
        return TraceDataset(links=trace_links)
