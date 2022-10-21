from typing import Callable, Dict, List, Set, Tuple

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from tracer.dataset.artifact import Artifact
from tracer.dataset.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from tracer.dataset.trace_dataset import TraceDataset
from tracer.dataset.trace_link import TraceLink
from tracer.pre_processing.pre_processor import PreProcessor


class ClassicTraceDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, source_layers: List[Dict[str, str]], target_layers: List[Dict[str, str]], pre_processor: PreProcessor,
                 true_links: List[Tuple[str, str]] = None, use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Constructs dataset in classic trace format
        :param source_layers: a list of source artifacts across all layers
        :param target_layers: a list of target artifacts across all layers
        :param true_links: list of tuples containing linked source and target ids
        :param pre_processor: the pre_processor to run on the data
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(pre_processor, use_linked_targets_only)
        self.source_layers = source_layers
        self.target_layers = target_layers
        self.true_links = true_links

    def create(self) -> TraceDataset:
        """
        Gets the dataset
        :return: the dataset
        """
        pos_link_ids = self._get_pos_link_ids(self.true_links) if self.true_links else set()
        all_links = self._generate_all_links(self.source_layers, self.target_layers, pos_link_ids)
        neg_link_ids = set(all_links.keys()).difference(pos_link_ids)
        return TraceDataset(links=all_links, pos_link_ids=list(pos_link_ids), neg_link_ids=list(neg_link_ids))

    def _generate_all_links(self, source_layers: List[Dict[str, str]], target_layers: List[Dict[str, str]],
                            pos_link_ids: Set[int]) -> Dict[int, TraceLink]:
        """
        Generates Trace Links between source and target pairs within each layer
        :param source_layers: a list of source artifacts across all layers
        :param target_layers: a list of target artifacts across all layers
        :param pos_link_ids: a set of all link ids corresponding to true links
        :return: a dictionary of the links, a list of the positive link ids, and a list of the negative link ids
        """
        links = {}
        for layer in range(len(source_layers)):
            source_artifacts = self._make_artifacts(source_layers[layer])
            target_artifacts = self._make_artifacts(target_layers[layer])
            layer_links = self._create_links_for_layer(source_artifacts, target_artifacts, pos_link_ids)
            links.update(layer_links)
        return links

    def _make_artifacts(self, artifacts_dict: Dict[str, str]) -> List[Artifact]:
        """
        Makes artifacts from a dictionary containing id, token information
        :param artifacts_dict: a dictionary containing id, token information
        :return: list of artifacts
        """
        artifacts = []
        for artifact_id, artifact_token in artifacts_dict.values():
            processed_artifact_token = self._process_tokens(artifact_token)
            artifacts.append(Artifact(artifact_id, processed_artifact_token))
        return artifacts
