from typing import Dict, Iterable, Set, Type

import pandas as pd

from config.override import overrides
from data.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.creators.readers.supported_dataset_reader import SupportedDatasetReader
from data.datasets.keys.structure_keys import StructuredKeys
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from util.base_object import BaseObject
from util.dataframe_util import DataFrameUtil
from util.reflection_util import ReflectionUtil
from util.uncased_dict import UncasedDict

ArtifactMap = Dict[str, Dict[str, Artifact]]


class TraceDatasetCreator(AbstractDatasetCreator[TraceDataset]):
    """
    Responsible for creating TraceDataset from DataFrames containing artifacts, traces, and
    layer mappings.
    """
    ALLOW_MISSING_SOURCE = False
    ALLOW_MISSING_TARGET = False

    def __init__(self, project_reader: AbstractProjectReader, data_cleaner: DataCleaner = None,
                 filter_unlinked_artifacts: bool = False):
        """
        Initializes creator with entities extracted from reader.
        :param project_reader: Project reader responsible for extracting project entities.
        :param data_cleaner: Data Cleaner containing list of data cleaning steps to perform on artifact tokens.
        :param filter_unlinked_artifacts: Whether to remove artifacts without a positive trace link.
        """
        super().__init__(data_cleaner)
        self.artifact_df = None
        self.trace_df = None
        self.layer_mapping_df = None
        self.project_reader = project_reader
        self.filter_unlinked_artifacts = filter_unlinked_artifacts

    def create(self) -> TraceDataset:
        """
        Creates TraceDataset with links.
        :return: TraceDataset.
        """
        self.artifact_df, self.trace_df, self.layer_mapping_df = self.project_reader.read_project()
        self.trace_df = DataFrameUtil.add_optional_column(self.trace_df, StructuredKeys.Trace.LABEL, 1)
        ReflectionUtil.set_attributes(self, self.project_reader.get_overrides())
        if self.filter_unlinked_artifacts:
            self._filter_unlinked_artifacts()
        self._filter_null_references()
        self._clean_artifact_tokens()
        return self._create_trace_dataset()

    @classmethod
    @overrides(BaseObject)
    def _get_child_enum_class(cls, abstract_class: Type, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        return SupportedDatasetReader

    def _filter_unlinked_artifacts(self):
        """
        Removes artifacts containing no positive links.
        :return: None
        """
        linked_artifact_ids = self._get_linked_artifact_ids(self.trace_df)
        self._remove_artifacts(linked_artifact_ids)

    def _filter_null_references(self) -> None:
        """
        Checks that trace links reference known artifacts.
        :return: None
        """
        valid_traces = self._filter_unreferenced_traces(self.artifact_df, self.trace_df, self.ALLOW_MISSING_SOURCE,
                                                        self.ALLOW_MISSING_TARGET)
        self.trace_df = pd.DataFrame(valid_traces)

    def _clean_artifact_tokens(self) -> None:
        """
        Performs data cleaning steps on artifact tokens and creates artifacts.
        :return: None
        """
        artifact_tokens = self.artifact_df[StructuredKeys.Artifact.BODY]
        artifact_tokens = self.data_cleaner.run(artifact_tokens)
        self.artifact_df[StructuredKeys.Artifact.BODY] = artifact_tokens

    def _create_trace_dataset(self) -> TraceDataset:
        """
        Creates trace links from trace DataFrame using artifacts for references.
        :return: Mapping of trace link ids to the link.
        """
        artifact_map: Dict[str, Dict[str, Artifact]] = UncasedDict()
        trace_dataset = self._create_trace_dataset_from_dataframe(artifact_map)
        if self.project_reader.should_generate_negative_links():
            self._generate_negative_links(self.layer_mapping_df, artifact_map, trace_dataset)
        return trace_dataset

    def _create_trace_dataset_from_dataframe(self, artifact_map: ArtifactMap) -> TraceDataset:
        """
        Creates trace links in DataFrame and constructs trace dataset containing them.
        :param artifact_map: Map of artifact type to artifact map (id to artifact).
        :return: TraceDataset containing links in trace dataframe.
        """
        trace_link_map = {}
        positive_link_ids = []
        negative_link_ids = []
        for _, row in self.trace_df.iterrows():
            source_row = self.artifact_df[self.artifact_df[StructuredKeys.Artifact.ID] == row[StructuredKeys.Trace.SOURCE]].iloc[0]
            target_row = self.artifact_df[self.artifact_df[StructuredKeys.Artifact.ID] == row[StructuredKeys.Trace.TARGET]].iloc[0]
            source_artifact = self._add_artifact_to_map(source_row, artifact_map)
            target_artifact = self._add_artifact_to_map(target_row, artifact_map)
            is_true_link = int(row[StructuredKeys.Trace.LABEL]) == 1
            trace_link = TraceLink(source_artifact, target_artifact, is_true_link=is_true_link)
            trace_link_map[trace_link.id] = trace_link
            if is_true_link:
                positive_link_ids.append(trace_link.id)
            else:
                negative_link_ids.append(trace_link.id)
        return TraceDataset(trace_link_map, pos_link_ids=positive_link_ids, neg_link_ids=negative_link_ids)

    def _remove_artifacts(self, artifact_ids: Set[str]) -> None:
        """
        Removes artifacts and trace links who are not referenced in artifact ids.
        :param artifact_ids: The ids of the artifacts to keep.
        :return: None
        """

        def filter_unlinked_artifact(row: pd.Series):
            assert StructuredKeys.Artifact.ID in row, f"Missing artifact id: {row.to_dict()}"
            return row[StructuredKeys.Artifact.ID] in artifact_ids

        def filter_unlinked_trace(row: pd.Series):
            return row[StructuredKeys.Trace.SOURCE] in artifact_ids and row[StructuredKeys.Trace.TARGET] in artifact_ids

        self.artifact_df = DataFrameUtil.filter_df(self.artifact_df, filter_unlinked_artifact)
        self.trace_df = DataFrameUtil.filter_df(self.trace_df, filter_unlinked_trace)

    @staticmethod
    def _generate_negative_links(layer_mapping_df: pd.DataFrame, artifact_map: ArtifactMap, trace_dataset: TraceDataset) -> None:
        """
        Compares source and target artifacts for each entry in layer mapping and generates negative links between them.
        :param layer_mapping_df: DataFrame containing the comparisons between artifact types present in project.
        :param artifact_map: Map of artifact type to artifact map (id to artifact).
        :param trace_dataset: The trace dataset to add negative links to.
        :return: None
        """
        for _, row in layer_mapping_df.iterrows():
            source_type = row[StructuredKeys.LayerMapping.SOURCE_TYPE]
            target_type = row[StructuredKeys.LayerMapping.TARGET_TYPE]
            source_artifacts: Iterable[Artifact] = artifact_map[source_type].values()
            target_artifacts: Iterable[Artifact] = artifact_map[target_type].values()
            for source_artifact in source_artifacts:
                for target_artifact in target_artifacts:
                    trace_link_id = TraceLink.generate_link_id(source_artifact.id, target_artifact.id)
                    if trace_link_id not in trace_dataset.links:
                        trace_dataset.add_link(TraceLink(source_artifact, target_artifact, is_true_link=False))
        trace_dataset.shuffle_link_ids()

    @staticmethod
    def _filter_unreferenced_traces(artifact_df: pd.DataFrame, trace_df: pd.DataFrame, allow_missing_sources: bool,
                                    allow_missing_targets: bool) -> pd.DataFrame:
        """
        Filters out trace links with references to unknown artifacts. Errors are thrown when flags are set to not allow null references.
        :param artifact_df: DataFrame containing artifacts.
        :param trace_df: DataFrame containing trace links.
        :param allow_missing_sources: If true, null references are removed. Otherwise,error is thrown if null source reference is encountered.
        :param allow_missing_targets: If true, null references are removed. Otherwise,error is thrown if null target reference is encountered.
        :return: DataFrame of trace links without links containing null references.
        """
        valid_traces = []
        valid_artifact_ids = artifact_df[StructuredKeys.Artifact.ID].values
        for _, row in trace_df.iterrows():
            source_id = row[StructuredKeys.Trace.SOURCE]
            target_id = row[StructuredKeys.Trace.TARGET]
            if source_id not in valid_artifact_ids:
                if not allow_missing_sources:
                    raise ValueError(f"Unknown source artifact reference: {source_id}")
            elif target_id not in valid_artifact_ids:
                if not allow_missing_targets:
                    raise ValueError(f"Unknown target artifact reference: {target_id}")
            else:
                valid_traces.append(row.to_dict())
        return pd.DataFrame(valid_traces)

    @staticmethod
    def _add_artifact_to_map(artifact_row: pd.Series, artifact_map: ArtifactMap) -> Artifact:
        """
        If non-existent, creates artifact and adds it to artifact map.
        :param artifact_row: The row in the artifact dataframe to create.
        :param artifact_map: The map of type to artifact map (id to artifact).
        :return: Artifact created or retrieved if existent.
        """
        artifact_id: str = artifact_row[StructuredKeys.Artifact.ID]
        artifact_type = artifact_row[StructuredKeys.Artifact.LAYER_ID]
        if artifact_type not in artifact_map:
            artifact_map[artifact_type] = UncasedDict()

        if artifact_id not in artifact_map[artifact_type]:
            artifact_body = artifact_row[StructuredKeys.Artifact.BODY]
            artifact_map[artifact_type][artifact_id] = Artifact(artifact_id, artifact_body)
        return artifact_map[artifact_type][artifact_id]

    @staticmethod
    def _get_linked_artifact_ids(trace_df) -> Set[str]:
        """
        Extracts set of artifact id containing at least one positive link.
        :return: Set of artifact ids.
        """
        linked_artifact_ids = set()
        for _, row in trace_df.iterrows():
            source_id = row[StructuredKeys.Trace.SOURCE]
            target_id = row[StructuredKeys.Trace.TARGET]
            is_true_link = int(row[StructuredKeys.Trace.LABEL]) == 1
            if is_true_link:
                linked_artifact_ids.update({source_id, target_id})
        return linked_artifact_ids

    @staticmethod
    def _set_index(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
        return df.reset_index().set_index(col_name)
