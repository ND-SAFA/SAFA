from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from data.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.creators.readers.project.structure_project_reader import StructureProjectReader
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner


class StructureDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, project_path: str,
                 data_cleaner: DataCleaner = None,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Creates a dataset from the coest.org website.
        :param project_path: Path to the project folder containing definition file.
        :param data_cleaner: The cleaner responsible for processing artifact tokens.
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(data_cleaner, use_linked_targets_only)
        self.project_path = project_path

    def create(self) -> TraceDataset:
        """
        Creates the coest dataset using the structured project reader
        :return: the dataset
        """
        return StructureProjectReader(self.project_path).create()
