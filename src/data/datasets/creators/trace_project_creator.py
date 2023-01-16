from typing import Callable, Dict, Set

import pandas as pd

from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.keys.structure_keys import StructureKeys
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner
from data.tree.artifact import Artifact


class TraceDatasetCreator:
    """
    Responsible for creating TraceDataset from DataFrames containing artifacts, traces, and
    layer mappings.
    """
    ALLOW_MISSING_SOURCE = False
    ALLOW_MISSING_TARGET = False

    def __init__(self, project_reader: AbstractProjectReader, data_cleaner: DataCleaner = None,
                 filter_unlinked_artifacts: bool = True):
        """
        Initializes creator with entities extracted from reader.
        :param project_reader: Project reader responsible for extracting project entities.
        :param data_cleaner: Data Cleaner containing list of data cleaning steps to perform on artifact tokens.
        :param filter_unlinked_artifacts: Whether to remove artifacts without a positive trace link.
        """
        self.artifact_df, self.trace_df, self.layer_mapping_df = project_reader.read_project()
        self.project_reader = project_reader
        self.filter_unlinked_artifacts = filter_unlinked_artifacts
        self.data_cleaner = DataCleaner([]) if data_cleaner is None else data_cleaner

    def create(self) -> TraceDataset:
        """
        Creates TraceDataset with links.
        :return: TraceDataset.
        """
        if self.filter_unlinked_artifacts:
            self._filter_unlinked_artifacts()
        self._filter_null_references()
        artifacts = self._create_and_clean_artifacts()
        return self._create_trace_dataset(artifacts)

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
        raise NotImplementedError()

    def _create_and_clean_artifacts(self) -> Dict[str, Artifact]:
        """
        Performs data cleaning steps on artifact tokens and creates artifacts.
        :return: List of artifacts.
        """
        raise NotImplementedError()

    def _create_trace_dataset(self, artifacts: Dict[str, Artifact]) -> TraceDataset:
        """
        Creates trace links from trace DataFrame using artifacts for references.
        :param artifacts: List of artifacts to reference when creating links.
        :return: Mapping of trace link ids to the link.
        """
        raise NotImplementedError()

    def _remove_artifacts(self, artifact_ids: Set[str]) -> None:
        """
        Removes artifacts and trace links who are not referenced in artifact ids.
        :param artifact_ids: The ids of the artifacts to keep.
        :return: None
        """

        def filter_unlinked_artifact(row: pd.Series):
            return row[StructureKeys.Artifact.ID] in artifact_ids

        def filter_unlinked_trace(row: pd.Series):
            return row[StructureKeys.Trace.SOURCE] in artifact_ids and row[StructureKeys.Trace.TARGET] in artifact_ids

        self.artifact_df = TraceDatasetCreator._filter_df(self.artifact_df, filter_unlinked_artifact)
        self.trace_df = TraceDatasetCreator._filter_df(self.trace_df, filter_unlinked_trace)

    @staticmethod
    def _get_linked_artifact_ids(trace_df) -> Set[str]:
        """
        Extracts set of artifact id containing at least one positive link.
        :return: Set of artifact ids.
        """
        linked_artifact_ids = set()
        for _, row in trace_df.iterrows():
            source_id = row[StructureKeys.Trace.SOURCE]
            target_id = row[StructureKeys.Trace.TARGET]
            is_true_link = int(row[StructureKeys.Trace.LABEL]) == 1
            if is_true_link:
                linked_artifact_ids.update({source_id, target_id})
        return linked_artifact_ids

    @staticmethod
    def _filter_df(df: pd.DataFrame, filter_lambda: Callable[[pd.Series], bool]) -> pd.DataFrame:
        """
        Returns DataFrame containing rows returning true in filter.
        :param df: The original DataFrame.
        :param filter_lambda: The lambda determining which rows to keep.
        :return: DataFrame containing filtered rows.
        """
        return df[df.apply(filter_lambda)]
