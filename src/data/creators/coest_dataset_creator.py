import os
from enum import Enum
from typing import Callable, Dict, List

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
from util.json_util import JSONUtil


def read_folder(folder_path: str, exclude=None):
    """
    Creates artifact for each file in folder path.
    :param folder_path: Path to folder containing artifact files.
    :param exclude: The files to exclude in folder path.
    :return: DataFrame containing artifact ids and tokens.
    """
    if exclude is None:
        exclude = [".DS_Store"]
    items = list(filter(lambda f: f not in exclude, os.listdir(folder_path)))
    entries = []
    for item in items:
        file_path = os.path.join(folder_path, item)
        entry = {
            SafaFormat.ARTIFACT_ID: item,
            SafaFormat.ARTIFACT_TOKEN: FileUtil.read_file(file_path)
        }
        entries.append(entry)
    return pd.DataFrame(entries)


class Wrapper:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)


class CoestParsers(Enum):
    XML = Wrapper(pd.read_xml)
    CSV = Wrapper(pd.read_csv)
    FOLDER = Wrapper(read_folder)


class CoestKeys:
    PARSER = "parser"
    COLS = "cols"
    FILE = "file"
    CONVERSIONS = "conversions"
    PARAMS = "params"


class CoestDataset:
    DEFINITION_FILE = "definition.json"

    def __init__(self, project_path: str):
        self.project_path = project_path
        self.definition_path = os.path.join(project_path, self.DEFINITION_FILE)
        self.dataset_name = os.path.split(project_path)[-1]
        self.dataset_definition = FileUtil.read_json_file(self.definition_path)
        self.conversions = self.dataset_definition[CoestKeys.CONVERSIONS]

    def get_artifacts(self):
        JSONUtil.require_properties(self.dataset_definition, [SafaFormat.ARTIFACTS])
        return self.dataset_definition[SafaFormat.ARTIFACTS].items()

    def get_traces(self):
        JSONUtil.require_properties(self.dataset_definition, [SafaFormat.TRACES])
        return self.dataset_definition[SafaFormat.TRACES].items()


def parse_file_definition(dataset: CoestDataset, file_definition: Dict) -> pd.DataFrame:
    """
    Reads and parses file from definition.
    :param dataset: The dataset to parse file from.
    :param file_definition: JSON detailing how to read the file.
    :return: DataFrame with parsed data.
    """
    required_properties = [CoestKeys.PARSER, CoestKeys.FILE]
    JSONUtil.require_properties(file_definition, required_properties)
    parser_name = file_definition[CoestKeys.PARSER].upper()
    parser = CoestParsers[parser_name].value
    file_rel_path = file_definition[CoestKeys.FILE]
    file_path = os.path.join(dataset.project_path, file_rel_path)

    params = file_definition[CoestKeys.PARAMS] if CoestKeys.PARAMS in file_definition else {}
    column_conversion = dataset.conversions[file_definition[CoestKeys.COLS]] \
        if CoestKeys.COLS in file_definition else None

    df = parser(file_path, **params)
    return DataFrameUtil.convert_df(df, column_conversion)


def create_artifacts_from_df(artifact_df: pd.DataFrame, processor: Callable[[str], str]) -> List[Artifact]:
    artifacts = []
    for row_index, row_artifact in artifact_df.iterrows():
        artifact_id = row_artifact[SafaFormat.ARTIFACT_ID]
        artifact_content = row_artifact[SafaFormat.ARTIFACT_TOKEN]
        artifact_tokens = processor(artifact_content)
        artifact = Artifact(artifact_id, artifact_tokens)
        artifacts.append(artifact)
    return artifacts


class ArtifactDefinition:
    def __init__(self, dataset: CoestDataset, artifact_definition: Dict, processor):
        artifact_df = parse_file_definition(dataset, artifact_definition)
        self.artifacts = create_artifacts_from_df(artifact_df, processor)

    def __iter__(self) -> Artifact:
        for artifact in self.artifacts:
            yield artifact


class TraceDefinition:
    def __init__(self,
                 dataset: CoestDataset,
                 trace_definition: Dict,
                 type2artifacts: Dict[str, ArtifactDefinition]):
        self.source_type = trace_definition[SafaFormat.SOURCE_ID]
        self.target_type = trace_definition[SafaFormat.TARGET_ID]
        source_type = trace_definition[SafaFormat.SOURCE_ID]
        target_type = trace_definition[SafaFormat.TARGET_ID]

        source_artifact_definition = type2artifacts[source_type]
        target_artifact_definition = type2artifacts[target_type]
        traces_df = parse_file_definition(dataset, trace_definition)

        positive_link_ids = []
        negative_link_ids = []
        trace_links: Dict[int, TraceLink] = {}
        for source_artifact in source_artifact_definition:
            for target_artifact in target_artifact_definition:
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
        self.trace_links = trace_links
        self.positive_link_ids = positive_link_ids
        self.negative_link_ids = negative_link_ids


class CoestDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, project_path: str,
                 data_cleaning_steps: List[AbstractDataProcessingStep] = None,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Creates a dataset from the coest.org website.
        :param project_path: Path to the project folder containing definition file.
        """
        super().__init__(data_cleaning_steps, use_linked_targets_only)
        self.dataset = CoestDataset(project_path)

    def create(self) -> TraceDataset:
        name2artifacts = {}
        for artifact_name, artifact_definition in self.dataset.get_artifacts():
            name2artifacts[artifact_name] = ArtifactDefinition(self.dataset,
                                                               artifact_definition,
                                                               self._process_tokens)

        trace_links = {}
        pos_link_ids = []
        neg_link_ids = []
        for trace_export_file_name, trace_definition in self.dataset.get_traces():
            trace_definition = TraceDefinition(self.dataset, trace_definition, name2artifacts)
            trace_links.update(trace_definition.trace_links)
            pos_link_ids.extend(trace_definition.positive_link_ids)
            neg_link_ids.extend(trace_definition.negative_link_ids)
        return TraceDataset(links=trace_links, pos_link_ids=pos_link_ids, neg_link_ids=neg_link_ids)
