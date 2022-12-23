from typing import List

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from data.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.creators.readers.project.structure_project_reader import StructureProjectReader
from data.datasets.trace_dataset import TraceDataset
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep


class CoestDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, project_path: str,
                 data_cleaning_steps: List[AbstractDataProcessingStep] = None,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Creates a dataset from the coest.org website.
        :param project_path: Path to the project folder containing definition file.
        """
        super().__init__(data_cleaning_steps, use_linked_targets_only)
        self.project_path = project_path

    def create(self) -> TraceDataset:
        return StructureProjectReader(self.project_path).create()
