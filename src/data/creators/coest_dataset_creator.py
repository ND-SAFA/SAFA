from typing import Callable, List

import pandas as pd

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from data.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.creators.parsers.definitions.structure_definition_parser import StructureDefinitionParser
from data.datasets.trace_dataset import TraceDataset
from data.formats.safa_format import SafaFormat
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from data.tree.artifact import Artifact


def create_artifacts_from_df(artifact_df: pd.DataFrame, processor: Callable[[str], str]) -> List[Artifact]:
    artifacts = []
    for row_index, row_artifact in artifact_df.iterrows():
        artifact_id = row_artifact[SafaFormat.ARTIFACT_ID]
        artifact_content = row_artifact[SafaFormat.SAFA_CVS_ARTIFACT_TOKEN]
        artifact_tokens = processor(artifact_content)
        artifact = Artifact(artifact_id, artifact_tokens)
        artifacts.append(artifact)
    return artifacts


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
        return StructureDefinitionParser(self.project_path).create()
