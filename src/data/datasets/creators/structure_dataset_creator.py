from data.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.creators.readers.definitions.structure_project_definition import StructureProjectDefinition
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner


class StructureDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, project_path: str,
                 data_cleaner: DataCleaner = None):
        """
        Creates a dataset from the structure.org website.
        :param project_path: Path to the project folder containing definition file.
        :param data_cleaner: The cleaner responsible for processing artifact tokens.
        """
        super().__init__(data_cleaner)
        self.project_path = project_path

    def create(self) -> TraceDataset:
        """
        Creates the structure dataset using the structured project reader
        :return: the dataset
        """
        return StructureProjectDefinition(self.project_path).read_project()
