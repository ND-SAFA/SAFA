from data.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.creators.readers.definitions.tim_project_definition import TimProjectDefinition
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner


class SafaDatasetCreator(AbstractTraceDatasetCreator):
    JSON_EXT = ".json"
    CSV_EXT = ".csv"

    def __init__(self, project_path: str, data_cleaner: DataCleaner = None):
        """
        Creates a data from the SAFA data format.
        :param project_path: the path to the project
        :param data_cleaner: the cleaner responsible for processing artifact tokens.
        """
        super().__init__(data_cleaner)
        self.project_path = project_path

    def create(self) -> TraceDataset:
        """
        Creates the data
        :return: the data
        """
        return TimProjectDefinition(self.project_path).read_project()
