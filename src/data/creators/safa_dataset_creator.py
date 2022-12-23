from typing import List

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from data.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.trace_dataset import TraceDataset
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from data.readers.project.tim_definition_reader import TimProjectReader


class SafaDatasetCreator(AbstractTraceDatasetCreator):
    JSON_EXT = ".json"
    CSV_EXT = ".csv"

    def __init__(self, project_path: str, data_cleaning_steps: List[AbstractDataProcessingStep] = None,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Creates a data from the SAFA data format.
        :param project_path: the path to the project
        :param data_cleaning_steps: tuple containing the desired pre-processing steps and related params
        :param data_keys: keys to use to access data
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(data_cleaning_steps, use_linked_targets_only)
        self.project_path = project_path

    def create(self) -> TraceDataset:
        """
        Creates the data
        :return: the data
        """
        return TimProjectReader(self.project_path).create()
