from typing import Dict, List, Set, Tuple, Type

import pandas as pd

from constants import ALLOWED_MISSING_SOURCES_DEFAULT, ALLOWED_MISSING_TARGETS_DEFAULT, ALLOWED_ORPHANS_DEFAULT, \
    NO_ORPHAN_CHECK_VALUE, REMOVE_ORPHANS_DEFAULT
from data.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.trace_dataset import TraceDataset
from data.keys.structure_keys import StructuredKeys
from data.processing.cleaning.data_cleaner import DataCleaner
from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.supported_dataset_reader import SupportedDatasetReader
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from util.base_object import BaseObject
from util.dataframe_util import DataFrameUtil
from util.general_util import ListUtil
from util.logging.logger_manager import logger
from util.override import overrides
from util.reflection_util import ReflectionUtil
from util.thread_util import ThreadUtil
from util.uncased_dict import UncasedDict

ArtifactType2Id = Dict[str, List[str]]
Id2Artifact = Dict[str, Artifact]


class TraceDatasetCreator(AbstractDatasetCreator[TraceDataset]):
    """
    Responsible for creating TraceDataset from DataFrames containing artifacts, traces, and
    layer mappings.
    """

    def __init__(self, project_reader: AbstractProjectReader, data_cleaner: DataCleaner = None,
                 remove_orphans: bool = REMOVE_ORPHANS_DEFAULT,
                 allowed_missing_sources: int = ALLOWED_MISSING_SOURCES_DEFAULT,
                 allowed_missing_targets: int = ALLOWED_MISSING_TARGETS_DEFAULT,
                 allowed_orphans: int = ALLOWED_ORPHANS_DEFAULT):
        """
        Initializes creator with entities extracted from reader.
        :param project_reader: Project reader responsible for extracting project entities.
        :param data_cleaner: Data Cleaner containing list of data cleaning steps to perform on artifact tokens.
        :param remove_orphans: Whether to remove artifacts without a positive trace link.
        """
        super().__init__(data_cleaner)
        self.allowed_missing_sources = allowed_missing_sources
        self.allowed_missing_targets = allowed_missing_targets
        self.allowed_orphans = allowed_orphans
        self.artifact_df = None
        self.trace_df = None
        self.layer_mapping_df = None
        self.project_reader = project_reader
        self.remove_orphans = remove_orphans
        self.linked_artifact_ids = None
        self.orphan_artifact_ids = None

    def create(self) -> TraceDataset:
        """
        Creates TraceDataset with links.
        :return: TraceDataset.
        """
        self.artifact_df, self.trace_df, self.layer_mapping_df = self.project_reader.read_project()
        self.trace_df = DataFrameUtil.add_optional_column(self.trace_df, StructuredKeys.Trace.LABEL, 1)
        overrides = self.project_reader.get_overrides()
        ReflectionUtil.set_attributes(self, overrides)
        self._verify_orphans()
        if self.remove_orphans:
            self._remove_orphans()
        self._filter_null_references()
        self._clean_artifact_tokens()
        trace_dataset = self._create_trace_dataset()
        TraceDatasetCreator._log_trace_dataset(trace_dataset)
        return trace_dataset

    def get_name(self) -> str:
        """
        :return: Returns the name of the project read in.
        """
        return self.project_reader.get_project_name()

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

    def _remove_orphans(self):
        """
        Removes artifacts containing no positive links.
        :return: None
        """
        linked_artifact_ids = self._get_linked_artifact_ids()
        self._verify_orphans()
        self._filter_artifacts_by_ids(linked_artifact_ids)

    def _get_orphan_artifact_ids(self) -> List[str]:
        """
        :return: Returns list of orphan artifact ids.
        """
        if self.orphan_artifact_ids is None:
            orphan_artifact_ids: Set = set()
            linked_artifact_ids = self._get_linked_artifact_ids()
            for i, row in self.artifact_df.iterrows():
                artifact_id = row[StructuredKeys.Artifact.ID]
                if artifact_id not in linked_artifact_ids:
                    orphan_artifact_ids.add(artifact_id)
            self.orphan_artifact_ids = list(orphan_artifact_ids)
        return self.orphan_artifact_ids

    def _filter_null_references(self) -> None:
        """
        Checks that trace links reference known artifacts.
        :return: None
        """
        valid_traces = self._filter_unreferenced_traces(self.artifact_df, self.trace_df,
                                                        self.allowed_missing_sources, self.allowed_missing_targets)
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

        def filter_by_id(row: pd.Series):
            assert StructuredKeys.Artifact.ID in row, f"Missing artifact id property ({StructuredKeys.Artifact.ID}): {row.to_dict()}"
            return row[StructuredKeys.Artifact.ID] in artifact_ids

        def remove_traces_with_missing_artifacts(row: pd.Series):
            return row[StructuredKeys.Trace.SOURCE] in artifact_ids and row[StructuredKeys.Trace.TARGET] in artifact_ids

        self.artifact_df = DataFrameUtil.filter_df(self.artifact_df, filter_by_id)
        self.trace_df = DataFrameUtil.filter_df(self.trace_df, remove_traces_with_missing_artifacts)

    def _verify_orphans(self) -> None:
        """
        Verifies that orphans lie below a certain threshold.
        :return: None
        """
        if self.allowed_orphans == NO_ORPHAN_CHECK_VALUE:
            return
        error_msg = f"Found too many orphan artifacts"
        default_msg = f"Number of orphan artifacts"
        TraceDatasetCreator.assert_artifact_less_than(self._get_orphan_artifact_ids(), self.allowed_orphans, error_msg, default_msg)

    def _get_linked_artifact_ids(self) -> Set[str]:
        """
        Extracts set of artifact id containing at least one positive link.
        :return: Set of artifact ids.
        """
        if self.linked_artifact_ids is None:
            linked_artifact_ids = set()
            for _, row in self.trace_df.iterrows():
                source_id = row[StructuredKeys.Trace.SOURCE]
                target_id = row[StructuredKeys.Trace.TARGET]
                is_true_link = int(row[StructuredKeys.Trace.LABEL]) == 1
                if is_true_link:
                    linked_artifact_ids.update({source_id, target_id})
            self.linked_artifact_ids = linked_artifact_ids
        return self.linked_artifact_ids

    @staticmethod
    def _generate_negative_links(layer_mapping_df: pd.DataFrame, artifact_type_2_id: ArtifactType2Id, id_2_artifact: Id2Artifact,
                                 trace_dataset: TraceDataset, n_threads=10) -> None:
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

            def create_target_links(artifact_id) -> None:
                """
                Create negative links for artifact against target artifacts.
                :param artifact_id: The id of the artifact to link to targets.
                :return:  None
                """
                artifact = id_2_artifact[artifact_id]
                for target_artifact_id in target_artifact_ids:
                    target_artifact = id_2_artifact[target_artifact_id]
                    trace_link_id = TraceLink.generate_link_id(artifact_id, target_artifact_id)
                    if trace_link_id not in trace_dataset.links:
                        trace_dataset.add_link(TraceLink(artifact, target_artifact, is_true_link=False))

            title = f"Generating negative links between {source_type} -> {target_type}"
            ThreadUtil.multi_thread_process(title, source_artifact_ids, create_target_links, n_threads)
        trace_dataset.shuffle_link_ids()

    @staticmethod
    def _filter_unreferenced_traces(artifact_df: pd.DataFrame, trace_df: pd.DataFrame, max_missing_sources: int,
                                    max_missing_targets: int) -> pd.DataFrame:
        """
        Filters out trace links with references to unknown artifacts. Errors are thrown when flags are set to not allow null references.
        :param artifact_df: DataFrame containing artifacts.
        :param trace_df: DataFrame containing trace links.
        :param max_missing_sources: The maximum number of allowed missing sources.
        :param max_missing_targets: The maximum number of allowed missing targets.
        :return: DataFrame of trace links without links containing null references.
        """
        valid_traces = []
        valid_artifact_ids = artifact_df[StructuredKeys.Artifact.ID].values
        missing_sources = []
        missing_targets = []
        for _, row in trace_df.iterrows():
            source_id = row[StructuredKeys.Trace.SOURCE]
            target_id = row[StructuredKeys.Trace.TARGET]
            if source_id not in valid_artifact_ids:
                missing_sources.append(source_id)
            elif target_id not in valid_artifact_ids:
                missing_targets.append(target_id)
            else:
                valid_traces.append(row.to_dict())

        TraceDatasetCreator.assert_missing_artifact_ids(missing_sources, max_missing_sources, "source")
        TraceDatasetCreator.assert_missing_artifact_ids(missing_targets, max_missing_targets, "target")
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

        for artifact_type, artifact_ids in artifact_type_2_id.items():
            logger.info(f"{artifact_type.title()}: {len(artifact_ids)}")
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
    def assert_missing_artifact_ids(missing_artifact_ids: List[str], max_missing_allowed: int, label: str) -> None:
        """
        Verifies that the missing artifacts does not exceed the maximum allowed.
        :param missing_artifact_ids: The ids of the missing artifacts.
        :param max_missing_allowed: The maximum allowed of missing artifacts.
        :param label: The label to group error with, if it exists.
        :return: None
        """
        error_msg = f"Found too null references to {label} artifacts ({len(missing_artifact_ids)})"
        default_msg = f"No missing {label} artifacts."
        TraceDatasetCreator.assert_artifact_less_than(missing_artifact_ids, max_missing_allowed, error_msg, default_msg)

    @staticmethod
    def assert_artifact_less_than(artifact_ids: List, n_allowed: int, error_msg: str, default_msg: str = None, n_items_per_line=10):
        """
        Asserts that artifacts ids are less than number allowed. Otherwise, error is thrown with error message.
        :param artifact_ids: The artifacts ids to verify.
        :param n_allowed: The maximum allowed of artifacts ids in list.
        :param error_msg: The error message to print if verification fails.
        :param default_msg: The message to display if artifacts are under threshold.
        :param n_items_per_line: How many items to print per line.
        :return: None
        """
        n_artifacts = len(artifact_ids)
        if n_artifacts > n_allowed:
            artifact_id_str = "\n".join(
                [",".join([str(a) for a in batch]) for batch in ListUtil.batch(artifact_ids, n_items_per_line)])
            raise ValueError(f"{error_msg}. Expected {n_allowed} but found {n_artifacts}.\n {artifact_id_str}")
        else:
            if default_msg:
                logger.info(f"{default_msg} ({n_artifacts})")

    @staticmethod
    def _log_trace_dataset(trace_dataset) -> None:
        """
        Logs dataset detailing the number of positive, negative, and total links it has.
        :param trace_dataset: The trace dataset containing links.
        :return: None
        """
        n_positive = len(trace_dataset.pos_link_ids)
        n_total = len(trace_dataset.links)
        n_negative = n_total - n_positive
        logger.info(f"Trace dataset(+{n_positive}, -({n_negative}) = {n_total})")
        return trace_dataset
