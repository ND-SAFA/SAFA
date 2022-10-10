from typing import Tuple, Dict, List, Callable, Iterable, Set

import pandas as pd

from common.models.model_generator import ModelGenerator
from trace.config.constants import VALIDATION_PERCENTAGE_DEFAULT
from trace.data.artifact import Artifact
from trace.data.dataset import Dataset
from trace.data.dataset_creators.abstract_dataset_creator import AbstractDatasetCreator
from trace.data.trace_link import TraceLink


class CSVKey:
    ID_PARAM = "ID"
    SOURCE_ID_PARAM = "source_id"
    TARGET_ID_PARAM = "target_id"
    CONTENT_PARAM = "Content"
    SOURCE_PARAM = "Source"
    TARGET_PARAM = "Target"
    TEXT_PARAM = "text"
    LABEL_PARAM = "label"


class CSVDatasetCreator(AbstractDatasetCreator):

    def __init__(self, data_file_path: str, model_generator: ModelGenerator,
                 validation_percentage: float = VALIDATION_PERCENTAGE_DEFAULT):
        """
        Constructs dataset in CSV format
        :param data_file_path: path to csv
        :param model_generator: the ModelGenerator
        :param validation_percentage: percentage of dataset used for validation, if no value is supplied then data will not be split
        """

        data_df = pd.read_csv(data_file_path)
        links = self._generate_all_links(data_df, model_generator.get_feature)
        pos_link_ids, neg_link_ids = self._get_pos_and_neg_links(links.values())
        linked_target_ids = self._get_linked_targets_only(pos_link_ids, links)
        self.dataset = Dataset(links=links, arch_type=model_generator.arch_type,
                               pos_link_ids=pos_link_ids, neg_link_ids=neg_link_ids,
                               linked_target_ids=linked_target_ids, validation_percentage=validation_percentage)

    def get_dataset(self) -> Dataset:
        """
        Gets the dataset
        :return: the dataset
        """
        return self.dataset

    @staticmethod
    def _generate_all_links(data_df: pd.Dataframe, feature_func: Callable) -> Dict[int, TraceLink]:
        """
        Generates Trace Links from the dataframe
        :param data_df: a dataframe containing artifact and link information
        :param feature_func: function from which the artifact features can be generated
        :return: a dictionary of the links, a list of the positive link ids, and a list of the negative link ids
        """
        links = {}
        for row_i, row in data_df.iterrows():
            source = Artifact(row[CSVKey.SOURCE_ID_PARAM], row[CSVKey.SOURCE_PARAM], feature_func)
            target = Artifact(row[CSVKey.TARGET_ID_PARAM], row[CSVKey.TARGET_PARAM], feature_func)
            is_true_link = row[CSVKey.LABEL_PARAM] == 1
            link = TraceLink(source, target, feature_func, is_true_link)
            links[link.id] = link
        return links

    @staticmethod
    def _get_pos_and_neg_links(all_links: Iterable[TraceLink]) -> Tuple[Set, Set]:
        """
        Creates a list of all positive and negative link ids
        :param all_links: list of TraceLinks
        :return: a set of the positive link ids, and a set of the negative link ids
        """
        linked_target_ids = set()
        pos_link_ids = set()
        neg_link_ids = set()
        for link in all_links:
            if link.is_true_link:
                pos_link_ids.add(link.id)
                linked_target_ids.add(link.target.id)
            else:
                neg_link_ids.add(link.id)
        return pos_link_ids, neg_link_ids

    @staticmethod
    def _get_linked_targets_only(pos_link_ids: Set[int], links: Dict[int, TraceLink]) -> Set:
        """
        Gets a set containing only ids of targets that are part of at least one positive link
        :param pos_link_ids: set of ids of true links
        :param links: dictionary mapping link ids to TraceLinks
        :return: a set containing only ids of targets that are part of at least one positive link
        """
        return {links.get(link_id).target.id for link_id in pos_link_ids}
