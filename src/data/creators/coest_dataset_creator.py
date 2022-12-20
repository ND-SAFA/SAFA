import os
from typing import Dict, List

import pandas as pd

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from data.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.trace_dataset import TraceDataset
from data.formats.safa_format import SafaFormat
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from util.dataframe_util import DataFrameUtil
from util.file_util import FileUtil


class CoestKeys:
    PARSER = "parser"
    COLS = "cols"
    FILE = "file"
    CONVERSIONS = "conversions"
    PARAMS = "params"


class CoestDatasetCreator(AbstractTraceDatasetCreator):
    DEFINITION_FILE = "definition.json"
    PARSERS = {
        "XML": pd.read_xml,
        "CSV": pd.read_csv
    }

    def __init__(self, project_path: str,
                 data_cleaning_steps: List[AbstractDataProcessingStep] = None,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Creates a dataset from the coest.org website.
        :param project_path: Path to the project folder containing definition file.
        """
        super().__init__(data_cleaning_steps, use_linked_targets_only)
        self.project_path = project_path
        self.definition_path = os.path.join(project_path, self.DEFINITION_FILE)
        self.dataset_name = os.path.split(project_path)[-1]

    def create(self) -> TraceDataset:
        dataset_definition = FileUtil.read_json_file(self.definition_path)
        conversions = dataset_definition[CoestKeys.CONVERSIONS]

        type2artifacts: Dict[str, List[Artifact]] = {}
        for artifact_name, artifact_definition in dataset_definition[SafaFormat.ARTIFACTS].items():
            artifact_df = self.parse_file(artifact_definition, conversions)
            artifacts = self.parse_artifacts(artifact_df)
            type2artifacts[artifact_name] = artifacts

        trace_links: Dict[int, TraceLink] = {}
        positive_link_ids = []
        negative_link_ids = []
        for trace_export_file_name, trace_definition in dataset_definition[SafaFormat.TRACES].items():
            source_type = trace_definition[SafaFormat.SOURCE_ID]
            target_type = trace_definition[SafaFormat.TARGET_ID]

            source_artifacts = type2artifacts[source_type]
            target_artifacts = type2artifacts[target_type]
            traces_df = self.parse_file(trace_definition, conversions)

            for source_artifact in source_artifacts:
                for target_artifact in target_artifacts:
                    source_id = source_artifact.id
                    target_id = target_artifact.id
                    trace_query = traces_df[(traces_df[SafaFormat.SOURCE_ID] == source_id) &
                                            (traces_df[SafaFormat.TARGET_ID] == target_id)]
                    is_positive = len(trace_query) >= 1
                    trace_link = TraceLink(source_artifact, target_artifact, is_true_link=is_positive)
                    if is_positive:
                        positive_link_ids.append(trace_link.id)
                    else:
                        negative_link_ids.append(trace_link.id)
                    trace_links[trace_link.id] = trace_link
        return TraceDataset(trace_links, pos_link_ids=positive_link_ids, neg_link_ids=negative_link_ids)

    @staticmethod
    def parse_artifacts(artifact_df: pd.DataFrame) -> List[Artifact]:
        artifacts = []
        for row_index, row_artifact in artifact_df.iterrows():
            artifact_id = row_artifact[SafaFormat.ARTIFACT_ID]
            artifact_content = row_artifact[SafaFormat.ARTIFACT_TOKEN]
            artifact = Artifact(artifact_id, artifact_content)
            artifacts.append(artifact)
        return artifacts

    def parse_file(self, file_definition: Dict, conversions: Dict) -> pd.DataFrame:
        parser = CoestDatasetCreator.PARSERS[file_definition[CoestKeys.PARSER]]
        params = file_definition[CoestKeys.PARAMS] if CoestKeys.PARAMS in file_definition else {}
        column_conversion = conversions[file_definition[CoestKeys.COLS]]
        file_rel_path = file_definition[CoestKeys.FILE]

        file_path = os.path.join(self.project_path, file_rel_path)
        df = parser(file_path, **params)
        return DataFrameUtil.convert_df(df, column_conversion)
