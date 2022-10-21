from abc import ABC, abstractmethod
from typing import List, Union, Set, Dict, Tuple

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from tracer.dataset.data_objects.artifact import Artifact
from tracer.dataset.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.dataset.trace_dataset import TraceDataset
from tracer.dataset.data_objects.trace_link import TraceLink
from tracer.pre_processing.pre_processor import PreProcessor


class AbstractTraceDatasetCreator(AbstractDatasetCreator, ABC):

    def __init__(self, pre_processor: PreProcessor, use_linked_targets_only: bool):
        """
        Responsible for creating dataset in format for defined models.
        :pre_processor: the pre_processor to run on the data
        :use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(pre_processor)
        self._linked_targets = set()
        self.use_linked_targets_only = use_linked_targets_only

    @abstractmethod
    def create(self) -> TraceDataset:
        """
        Creates the trace dataset
        :return: the dataset
        """
        pass

    def _create_links_for_layer(self, source_artifacts: List[Artifact], target_artifacts: List[Artifact],
                                pos_link_ids: Set[int]) -> Dict[int, TraceLink]:
        """
        Creates map between trace link id to trace link.
        :param source_artifacts: The source artifacts to extract links for.
        :param target_artifacts: The target artifacts to extract links for.
        :param pos_link_ids: The list of all positive link ids in project.
        :return: Map between trace link ids and trace links for given source and target artifacts.
        """
        if self.use_linked_targets_only:
            target_artifacts = self._filter_unlinked_targets(target_artifacts)

        links = {}
        for source in source_artifacts:
            for target in target_artifacts:
                link = TraceLink(source, target)
                link.is_true_link = link.id in pos_link_ids
                links[link.id] = link
        return links

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
