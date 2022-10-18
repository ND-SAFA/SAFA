from typing import Callable, Dict, Iterable, Set, Tuple

import pandas as pd

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from tracer.dataset.artifact import Artifact
from tracer.dataset.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.dataset.trace_dataset import TraceDataset
from tracer.dataset.trace_link import TraceLink
from tracer.models.model_generator import ModelGenerator


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
        :param validation_percentage: percentage of dataset used for validation, if no value is supplied then dataset will not be split
        """

        data_df = pd.read_csv(data_file_path)
        links = self._generate_all_links(data_df, model_generator.get_feature)
        pos_link_ids, neg_link_ids = self._get_pos_and_neg_links(links.values())
        self.arch_type = model_generator.arch_type
        self.validation_percentage = validation_percentage
        self.dataset = TraceDataset(links=links,
                                    pos_link_ids=list(pos_link_ids), neg_link_ids=list(neg_link_ids))

    def create(self) -> TraceDataset:
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
