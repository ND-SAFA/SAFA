from typing import Dict, List, Set, Tuple

from data.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink


class ClassicTraceDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, source_layers: List[Dict[str, str]], target_layers: List[Dict[str, str]],
                 true_links: List[Tuple[str, str]] = None,
                 data_cleaner: DataCleaner = None):
        """
        Constructs data in classic trace format
        :param source_layers: a list of source artifacts across all layers
        :param target_layers: a list of target artifacts across all layers
        :param true_links: list of tuples containing linked source and target ids
        :param data_cleaner: The cleaner responsible for processing artifact tokens.
        """
        super().__init__(data_cleaner)
        self.source_layers = source_layers
        self.target_layers = target_layers
        self.true_links = true_links

    def create(self) -> TraceDataset:
        """
        Gets the data
        :return: the data
        """
        pos_link_ids = self._get_pos_link_ids(self.true_links) if self.true_links else set()
        all_links = self._generate_all_links(self.source_layers, self.target_layers, pos_link_ids)
        return TraceDataset(links=all_links, randomize=True)

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
        for artifact_id, artifact_token in artifacts_dict.items():
            processed_artifact_token = self._process_tokens(artifact_token)
            artifacts.append(Artifact(artifact_id, processed_artifact_token))
        return artifacts

    @staticmethod
    def _create_links_for_layer(source_artifacts: List[Artifact], target_artifacts: List[Artifact],
                                pos_link_ids: Set[int]) -> Dict[int, TraceLink]:
        """
        Creates map between trace link id to trace link.
        :param source_artifacts: The source artifacts to extract links for.
        :param target_artifacts: The target artifacts to extract links for.
        :param pos_link_ids: The list of all positive link ids in project.
        :return: Map between trace link ids and trace links for given source and target artifacts.
        """

        links = {}
        for source in source_artifacts:
            for target in target_artifacts:
                link = TraceLink(source, target)
                link.is_true_link = link.id in pos_link_ids
                links[link.id] = link
        return links

    @staticmethod
    def _get_pos_link_ids(true_links: List[Tuple[str, str]]) -> Set[int]:
        """
        Creates a set of all positive and negative link ids
        :param true_links: list of tuples containing linked source and target ids
        :return: a list of the positive link ids, and a list of the negative link ids
        """
        pos_link_ids = set()
        for source_id, target_id in true_links:
            link_id = TraceLink.generate_link_id(source_id, target_id)
            pos_link_ids.add(link_id)
        return pos_link_ids
