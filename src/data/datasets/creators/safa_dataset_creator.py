from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from data.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.creators.readers.project.tim_project_reader import TimProjectReader
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner


class SafaDatasetCreator(AbstractTraceDatasetCreator):
    JSON_EXT = ".json"
    CSV_EXT = ".csv"

    def __init__(self, project_path: str, data_cleaner: DataCleaner = None,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Creates a data from the SAFA data format.
        :param project_path: the path to the project
        :param data_cleaner: the cleaner responsible for processing artifact tokens.
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(data_cleaner, use_linked_targets_only)
        self.project_path = project_path

    def create(self) -> TraceDataset:
        """
        Creates the data
        :return: the data
        """
        return TimProjectReader(self.project_path).create()
