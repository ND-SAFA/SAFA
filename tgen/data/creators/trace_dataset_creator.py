from collections import Counter
from typing import Any, Dict, List, Optional, Set

import pandas as pd

from tgen.constants.dataset_constants import ALLOWED_MISSING_SOURCES_DEFAULT, ALLOWED_MISSING_TARGETS_DEFAULT, ALLOWED_ORPHANS_DEFAULT, \
    NO_CHECK_VALUE, REMOVE_ORPHANS_DEFAULT
from tgen.constants.deliminator_constants import COMMA, NEW_LINE
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.processing.cleaning.data_cleaner import DataCleaner
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.dict_util import ListUtil
from tgen.util.logging.logger_manager import logger
from tgen.util.reflection_util import ReflectionUtil
from tgen.util.thread_util import ThreadUtil


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
        self.artifact_df: Optional[ArtifactDataFrame] = None
        self.trace_df: Optional[TraceDataFrame] = None
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
        self.process_data()
        trace_dataset = self._create_trace_dataset()
        TraceDatasetCreator._log_trace_dataset(trace_dataset)
        return trace_dataset

    def export_as_safa(self, export_path: str):
        """
        Exports project as safa project to directory given.
        :return:
        """

    def process_data(self):
        """
        Creates the necessary tables and performs validation checks on the data.
        :return:  None
        """
        self.artifact_df, self.trace_df, self.layer_mapping_df = self.project_reader.read_project()
        overrides = self.project_reader.get_overrides()
        ReflectionUtil.set_attributes(self, overrides)
        self._verify_orphans()
        if self.remove_orphans:
            self._remove_orphans()
        self._filter_null_references()
        self._clean_artifact_tokens()

    def get_name(self) -> str:
        """
        :return: Returns the name of the project read in.
        """
        return self.project_reader.get_project_name()

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
            self.orphan_artifact_ids = set(self.artifact_df.index).difference(self._get_linked_artifact_ids())
        return self.orphan_artifact_ids

    def _filter_null_references(self) -> None:
        """
        Checks that trace links reference known artifacts.
        :return: None
        """
        self.trace_df = self._filter_unreferenced_traces(self.artifact_df, self.trace_df,
                                                         self.allowed_missing_sources, self.allowed_missing_targets)

    def _clean_artifact_tokens(self) -> None:
        """
        Performs data cleaning steps on artifact tokens and creates artifacts.
        :return: None
        """
        artifact_tokens = self.artifact_df[StructuredKeys.Artifact.CONTENT]
        artifact_tokens = self.data_cleaner.run(artifact_tokens)
        self.artifact_df[StructuredKeys.Artifact.CONTENT] = artifact_tokens

    def _create_trace_dataset(self) -> TraceDataset:
        """
        Creates trace links from trace DataFrame using artifacts for references.
        :return: Mapping of trace link ids to the link.
        """
        if self.trace_df.get_label_count(0) < 1:
            self.trace_df = self.generate_negative_links(self.layer_mapping_df, self.artifact_df, self.trace_df)
        self._log_artifact_types(self.artifact_df)
        trace_dataset = TraceDataset(artifact_df=self.artifact_df, trace_df=self.trace_df, layer_df=self.layer_mapping_df)
        return trace_dataset

    def _filter_artifacts_by_ids(self, artifact_ids: Set[str]) -> None:
        """
        Removes artifacts and trace links who are not referenced in artifact ids.
        :param artifact_ids: The ids of the artifacts to keep.
        :return: None
        """

        def remove_traces_with_missing_artifacts(row: pd.Series):
            return row[StructuredKeys.Trace.SOURCE.value] in artifact_ids and row[StructuredKeys.Trace.TARGET.value] in artifact_ids

        self.artifact_df = ArtifactDataFrame(DataFrameUtil.filter_df_by_index(self.artifact_df, list(artifact_ids)))
        self.trace_df = TraceDataFrame(DataFrameUtil.filter_df_by_row(self.trace_df, remove_traces_with_missing_artifacts))

    def _verify_orphans(self) -> None:
        """
        Verifies that orphans lie below a certain threshold.
        :return: None
        """
        if self.allowed_orphans == NO_CHECK_VALUE:
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
            true_links = TraceDataFrame(self.trace_df[self.trace_df[StructuredKeys.Trace.LABEL] == 1])
            self.linked_artifact_ids = set(true_links[StructuredKeys.Trace.SOURCE]).union(true_links[StructuredKeys.Trace.TARGET])
        return self.linked_artifact_ids

    @staticmethod
    def generate_negative_links(layer_mapping_df: LayerDataFrame, artifact_df: ArtifactDataFrame,
                                trace_df: TraceDataFrame, n_threads=10) -> TraceDataFrame:
        """
        Compares source and target artifacts for each entry in layer mapping and generates negative links between them.
        :param layer_mapping_df: DataFrame containing the comparisons between artifact types present in project.
        :param artifact_df: DataFrame containing information about the artifacts in the project.
        :param trace_df: DataFrame containing true links present in project.
        :param n_threads: The maximum number of threads to use for pre-processing.
        :return: None
        """
        negative_links: Dict[int, Dict[TraceKeys, Any]] = {}

        for _, row in layer_mapping_df.itertuples():
            source_type = row[StructuredKeys.LayerMapping.SOURCE_TYPE]
            target_type = row[StructuredKeys.LayerMapping.TARGET_TYPE]
            source_artifact_ids = artifact_df[artifact_df[ArtifactKeys.LAYER_ID] == source_type].index
            target_artifact_ids = artifact_df[artifact_df[ArtifactKeys.LAYER_ID] == target_type].index
            assert len(source_artifact_ids) > 0, f"Expected at least one source artifact of type {source_type}"
            assert len(target_artifact_ids) > 0, f"Expected at least one target artifact of type {target_type}"

            def create_target_links(artifact_id) -> None:
                """
                Create negative links for artifact against target artifacts.
                :param artifact_id: The id of the artifact to link to targets.
                :return:  None
                """
                artifact = artifact_df.get_artifact(artifact_id)
                for target_artifact_id in target_artifact_ids:
                    target_artifact = artifact_df.get_artifact(target_artifact_id)
                    trace_link_id = TraceDataFrame.generate_link_id(artifact_id, target_artifact_id)
                    if trace_link_id not in trace_df.index and artifact_id != target_artifact_id:
                        negative_links[trace_link_id] = trace_df.link_as_dict(source_id=artifact[ArtifactKeys.ID],
                                                                              target_id=target_artifact[ArtifactKeys.ID],
                                                                              label=0)

            title = f"Generating negative links between {source_type} -> {target_type}"
            ThreadUtil.multi_thread_process(title, source_artifact_ids, create_target_links, n_threads)
        all_links = trace_df.to_dict(orient="index")
        all_links.update(negative_links)
        return TraceDataFrame.from_dict(all_links, orient="index")

    @staticmethod
    def _filter_unreferenced_traces(artifact_df: ArtifactDataFrame, trace_df: TraceDataFrame, max_missing_sources: int,
                                    max_missing_targets: int) -> TraceDataFrame:
        """
        Filters out trace links with references to unknown artifacts. Errors are thrown when flags are set to not allow null references.
        :param artifact_df: DataFrame containing artifacts.
        :param trace_df: DataFrame containing trace links.
        :param max_missing_sources: The maximum number of allowed missing sources.
        :param max_missing_targets: The maximum number of allowed missing targets.
        :return: DataFrame of trace links without links containing null references.
        """
        valid_traces = []
        valid_artifact_ids = set(artifact_df.index)
        missing_sources = []
        missing_targets = []
        for _, row in trace_df.itertuples():
            source_id = row[StructuredKeys.Trace.SOURCE]
            target_id = row[StructuredKeys.Trace.TARGET]
            if source_id not in valid_artifact_ids:
                missing_sources.append(source_id)
            elif target_id not in valid_artifact_ids:
                missing_targets.append(target_id)
            else:
                valid_traces.append(row)

        TraceDatasetCreator.assert_missing_artifact_ids(missing_sources, max_missing_sources, "source")
        TraceDatasetCreator.assert_missing_artifact_ids(missing_targets, max_missing_targets, "target")
        return TraceDataFrame(valid_traces)

    @staticmethod
    def assert_missing_artifact_ids(missing_artifact_ids: List[str], max_missing_allowed: int, label: str) -> None:
        """
        Verifies that the missing artifacts does not exceed the maximum allowed.
        :param missing_artifact_ids: The ids of the missing artifacts.
        :param max_missing_allowed: The maximum allowed of missing artifacts.
        :param label: The label to group error with, if it exists.
        :return: None
        """
        if max_missing_allowed == NO_CHECK_VALUE:
            return
        error_msg = f"Found too many null references to {label} artifacts ({len(missing_artifact_ids)})"
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
        artifact_ids = list(set(artifact_ids))
        n_artifacts = len(artifact_ids)
        if n_artifacts > n_allowed:
            artifact_id_str = NEW_LINE.join(
                [COMMA.join([str(a) for a in batch]) for batch in ListUtil.batch(artifact_ids, n_items_per_line)])
            raise ValueError(f"{error_msg}. Expected {n_allowed} but found {n_artifacts}.\n {artifact_id_str}")
        else:
            if default_msg:
                logger.info(f"{default_msg} ({n_artifacts})")

    @staticmethod
    def _log_artifact_types(artifact_df: ArtifactDataFrame) -> None:
        """
        Logs the number of artifacts of each type in the project
        :param artifact_df: The dataframe containing artifact information
        :return: None
        """
        artifact_type_summary = []
        counter = Counter(artifact_df.layer_id)
        for layer_id, count in counter.items():
            artifact_type_summary.append(f"[{layer_id.title()}: {count}]")
        logger.info(COMMA.join(artifact_type_summary))

    @staticmethod
    def _log_trace_dataset(trace_dataset: TraceDataset) -> None:
        """
        Logs dataset detailing the number of positive, negative, and total links it has.
        :param trace_dataset: The trace dataset containing links.
        :return: None
        """

        n_total = len(trace_dataset)
        n_positive = trace_dataset.trace_df.get_label_count(1)
        n_negative = trace_dataset.trace_df.get_label_count(0)
        logger.info(f"Trace dataset(+{n_positive}, -({n_negative}) = {n_total})")
