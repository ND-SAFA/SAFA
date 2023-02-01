from typing import Dict, List, Set, Tuple, Type

import pandas as pd

from config.constants import ALLOW_MISSING_SOURCE, ALLOW_MISSING_TARGET
from config.override import overrides
from data.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.supported_dataset_reader import SupportedDatasetReader
from data.keys.structure_keys import StructuredKeys
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from util.base_object import BaseObject
from util.dataframe_util import DataFrameUtil
from util.reflection_util import ReflectionUtil
from util.uncased_dict import UncasedDict

ArtifactType2Id = Dict[str, List[str]]
Id2Artifact = Dict[str, Artifact]


class TraceDatasetCreator(AbstractDatasetCreator[TraceDataset]):
    """
    Responsible for creating TraceDataset from DataFrames containing artifacts, traces, and
    layer mappings.
    """

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
        self.should_filter_unlinked_artifacts = filter_unlinked_artifacts

    def create(self) -> TraceDataset:
        """
        Creates TraceDataset with links.
        :return: TraceDataset.
        """
        self.artifact_df, self.trace_df, self.layer_mapping_df = self.project_reader.read_project()
        self.trace_df = DataFrameUtil.add_optional_column(self.trace_df, StructuredKeys.Trace.LABEL, 1)
        ReflectionUtil.set_attributes(self, self.project_reader.get_overrides())
        if self.should_filter_unlinked_artifacts:
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
        self._filter_artifacts_by_ids(linked_artifact_ids)

    def _filter_null_references(self) -> None:
        """
        Checks that trace links reference known artifacts.
        :return: None
        """
        valid_traces = self._filter_unreferenced_traces(self.artifact_df, self.trace_df, ALLOW_MISSING_SOURCE,
                                                        ALLOW_MISSING_TARGET)
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
        artifact_type_2_id, id_2_artifact = self._create_artifact_maps(self.artifact_df)
        trace_dataset = self._create_trace_dataset_from_dataframe(id_2_artifact)
        if self.project_reader.should_generate_negative_links():
            self._generate_negative_links(self.layer_mapping_df, artifact_type_2_id, id_2_artifact, trace_dataset)
        return trace_dataset

    def _create_trace_dataset_from_dataframe(self, id_2_artifact: Id2Artifact) -> TraceDataset:
        """
        Creates trace links in DataFrame and constructs trace dataset containing them.
        :param id_2_artifact: Map of artifact type to artifact id.
        :return: TraceDataset containing links in trace dataframe.
        """
        trace_link_map = {}
        positive_link_ids = []
        negative_link_ids = []
        for _, row in self.trace_df.iterrows():
            source_id = row[StructuredKeys.Trace.SOURCE]
            target_id = row[StructuredKeys.Trace.TARGET]
            source_artifact = id_2_artifact[source_id]
            target_artifact = id_2_artifact[target_id]
            is_true_link = int(row[StructuredKeys.Trace.LABEL]) == 1
            trace_link = TraceLink(source_artifact, target_artifact, is_true_link=is_true_link)
            trace_link_map[trace_link.id] = trace_link
            if is_true_link:
                positive_link_ids.append(trace_link.id)
            else:
                negative_link_ids.append(trace_link.id)
        return TraceDataset(trace_link_map, pos_link_ids=positive_link_ids, neg_link_ids=negative_link_ids)

    def _filter_artifacts_by_ids(self, artifact_ids: Set[str]) -> None:
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
    def _generate_negative_links(layer_mapping_df: pd.DataFrame, artifact_type_2_id: ArtifactType2Id, id_2_artifact: Id2Artifact,
                                 trace_dataset: TraceDataset) -> None:
        """
        Compares source and target artifacts for each entry in layer mapping and generates negative links between them.
        :param layer_mapping_df: DataFrame containing the comparisons between artifact types present in project.
        :param artifact_type_2_id: Map of artifact type to artifact ids associated with it.
        :param id_2_artifact: Map of artifact id to their associated artifact.
        :param trace_dataset: The trace dataset to add negative links to.
        :return: None
        """
        for _, row in layer_mapping_df.iterrows():
            source_type = row[StructuredKeys.LayerMapping.SOURCE_TYPE]
            target_type = row[StructuredKeys.LayerMapping.TARGET_TYPE]
            source_artifact_ids: List[str] = artifact_type_2_id[source_type]
            target_artifact_ids: List[str] = artifact_type_2_id[target_type]

            for source_artifact_id in source_artifact_ids:
                source_artifact = id_2_artifact[source_artifact_id]
                for target_artifact_id in target_artifact_ids:
                    target_artifact = id_2_artifact[target_artifact_id]
                    trace_link_id = TraceLink.generate_link_id(source_artifact_id, target_artifact_id)
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
    def _create_artifact_maps(artifact_df: pd.DataFrame) -> Tuple[ArtifactType2Id, Id2Artifact]:
        """
        Create mapping between artifact types and their associated artifacts and between artifact ids and their associated artifact.
        :param artifact_df: The data frame containing artifact data.
        :return: Map containing artifacts types and their associated artifacts.
        """
        artifact_type_2_id: ArtifactType2Id = UncasedDict()
        id_2_artifact: Id2Artifact = UncasedDict()
        for _, row in artifact_df.iterrows():
            TraceDatasetCreator._add_artifact_to_maps(row, artifact_type_2_id, id_2_artifact)
        return artifact_type_2_id, id_2_artifact

    @staticmethod
    def _add_artifact_to_maps(artifact_row: pd.Series, artifact_type_2_id: ArtifactType2Id, id_2_artifact: Id2Artifact) -> Artifact:
        """
        If non-existent, creates artifact and adds it to artifact map.
        :param artifact_row: The row in the artifact dataframe to create.
        :param artifact_type_2_id: The map of type to artifact id.
        :param id_2_artifact: The map between artifact ids and their associated artifact.
        :return: Artifact created or retrieved if existent.
        """
        artifact_id: str = artifact_row[StructuredKeys.Artifact.ID]
        artifact_type = artifact_row[StructuredKeys.Artifact.LAYER_ID]
        if artifact_type not in artifact_type_2_id:
            artifact_type_2_id[artifact_type] = []

        if artifact_id not in id_2_artifact:
            artifact_body = artifact_row[StructuredKeys.Artifact.BODY]
            artifact_type_2_id[artifact_type].append(artifact_id)
            id_2_artifact[artifact_id] = Artifact(artifact_id, artifact_body)
        return id_2_artifact[artifact_id]

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
