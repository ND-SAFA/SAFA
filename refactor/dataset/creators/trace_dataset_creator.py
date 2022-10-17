from typing import Callable, Dict, List, Set, Tuple

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from dataset.artifact import Artifact
from dataset.dataset_creators.abstract_dataset_creator import AbstractDatasetCreator
from dataset.trace_dataset import TraceDataset
from dataset.trace_link import TraceLink
from models.model_generator import ModelGenerator


class TraceDatasetCreator(AbstractDatasetCreator):

    def __init__(self, source_layers: List[Dict[str, str]], target_layers: List[Dict[str, str]],
                 model_generator: ModelGenerator, true_links: List[Tuple[str, str]] = None,
                 validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT):
        """
        Constructs dataset in classic trace format
        :param source_layers: a list of source artifacts across all layers
        :param target_layers: a list of target artifacts across all layers
        :param true_links: list of tuples containing linked source and target ids
        :param model_generator: the ModelGenerator
        :param validation_percentage: percentage of dataset used for validation, if no value is supplied then dataset will not be split
        """
        links = self._generate_all_links(source_layers, target_layers, model_generator.get_feature)
        pos_link_ids, neg_link_ids = self._get_pos_and_neg_links(true_links, links) if true_links else (None, None)
        linked_target_ids = self._get_linked_targets_only(true_links) if true_links else set()
        self.dataset = TraceDataset(links=links, arch_type=model_generator.arch_type,
                                    pos_link_ids=pos_link_ids, neg_link_ids=neg_link_ids,
                                    linked_target_ids=linked_target_ids, validation_percentage=validation_percentage)

    def get_dataset(self) -> TraceDataset:
        """
        Gets the dataset
        :return: the dataset
        """
        return self.dataset

    @staticmethod
    def _generate_all_links(source_layers: List[Dict[str, str]], target_layers: List[Dict[str, str]],
                            feature_func: Callable) \
            -> Dict[int, TraceLink]:
        """
        Generates Trace Links between source and target pairs within each layer
        :param source_layers: a list of source artifacts across all layers
        :param target_layers: a list of target artifacts across all layers
        :param feature_func: function from which the artifact features can be generated
        :return: a dictionary of the links, a list of the positive link ids, and a list of the negative link ids
        """
        links = {}
        for layer in range(len(source_layers)):
            layer_links = TraceDatasetCreator._make_links(source_layers[layer], target_layers[layer], feature_func)
            links.update(layer_links)
        return links

    @staticmethod
    def _make_links(source_artifacts: Dict[str, str], target_artifacts: Dict[str, str], feature_func: Callable) \
            -> Dict[int, TraceLink]:
        """
        Creates Trace Links from all source and target pairs
        :param source_artifacts: source artifacts represented as id, token mappings
        :param target_artifacts: target artifacts represented as id, token mappings
        :param feature_func: function from which the artifact features can be generated
        :return: a dictionary of the id, link mappings
        """
        links = {}
        for s_id, s_token in source_artifacts.items():
            source = Artifact(s_id, s_token, feature_func)
            for t_id, t_token in target_artifacts.items():
                target = Artifact(t_id, t_token, feature_func)
                link = TraceLink(source, target, feature_func)
                links[link.id] = link
        return links

    @staticmethod
    def _get_pos_and_neg_links(true_links: List[Tuple[str, str]], all_links: Dict[int, TraceLink]) -> Tuple[Set, Set]:
        """
        Creates a set of all positive and negative link ids
        :param true_links: list of tuples containing linked source and target ids
        :param all_links: dictionary of all possible TraceLinks
        :return: a list of the positive link ids, and a list of the negative link ids
        """
        pos_link_ids = set()
        for s_id, t_id in true_links:
            link_id = TraceLink.generate_link_id(s_id, t_id)
            true_link = all_links.get(link_id, None)
            if true_link:
                true_link.is_true_link = True
                pos_link_ids.add(link_id)
        neg_link_ids = set(all_links.keys()).difference(pos_link_ids)
        return pos_link_ids, neg_link_ids

    @staticmethod
    def _get_linked_targets_only(true_links: List) -> Set:
        """
        Gets a set containing only ids of targets that are part of at least one positive link
        :param true_links: list of tuples containing linked source and target ids
        :return: a set containing only ids of targets that are part of at least one positive link
        """
        return {t_id for _, t_id in true_links}
