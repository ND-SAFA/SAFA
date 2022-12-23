from abc import ABC, abstractmethod
from typing import List, Set, Tuple

from data.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink


class AbstractTraceDatasetCreator(AbstractDatasetCreator, ABC):

    def __init__(self, data_cleaner: DataCleaner, use_linked_targets_only: bool):
        """
        Responsible for creating data in format for defined models.
        :param data_cleaner: Processes the artifact tokens.
        :use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(data_cleaner)
        self._linked_targets = set()
        self._use_linked_targets_only = use_linked_targets_only

    @abstractmethod
    def create(self) -> TraceDataset:
        """
        Creates the trace data
        :return: the data
        """
        pass

    def _get_pos_link_ids(self, true_links: List[Tuple[str, str]]) -> Set[int]:
        """
        Creates a set of all positive and negative link ids
        :param true_links: list of tuples containing linked source and target ids
        :return: a list of the positive link ids, and a list of the negative link ids
        """
        pos_link_ids = set()
        for source_id, target_id in true_links:
            link_id = TraceLink.generate_link_id(source_id, target_id)
            pos_link_ids.add(link_id)
            self._linked_targets.add(target_id)
        return pos_link_ids

    def _filter_unlinked_targets(self, all_target_artifacts: List[Artifact]) -> List[Artifact]:
        """
        Gets only the target artifacts that are part of at least one true link
        :param all_target_artifacts: a list of all target artifacts
        :return: a list of linked target artifacts only
        """
        return [artifact for artifact in all_target_artifacts if artifact.id in self._linked_targets]
