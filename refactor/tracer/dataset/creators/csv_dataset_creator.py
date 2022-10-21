from typing import List

import pandas as pd

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from tracer.dataset.data_objects.artifact import Artifact
from tracer.dataset.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from tracer.dataset.trace_dataset import TraceDataset
from tracer.dataset.data_objects.trace_link import TraceLink
from tracer.pre_processing.pre_processor import PreProcessor


class CSVKey:
    ID_PARAM = "ID"
    SOURCE_ID_PARAM = "source_id"
    TARGET_ID_PARAM = "target_id"
    CONTENT_PARAM = "Content"
    SOURCE_PARAM = "Source"
    TARGET_PARAM = "Target"
    TEXT_PARAM = "text"
    LABEL_PARAM = "label"


class CSVDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, data_file_path: str, pre_processor: PreProcessor,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Constructs dataset in CSV format
        :param data_file_path: path to csv
        :param pre_processor: the pre_processor to run on the data
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(pre_processor, use_linked_targets_only)
        self.data_file_path = data_file_path

    def create(self) -> TraceDataset:
        """
        Creates the dataset
        :return: the dataset
        """
        data_df = pd.read_csv(self.data_file_path)
        links = {}
        pos_link_ids, neg_link_ids = [], []
        for i, row in data_df.iterrows():
            source_tokens, target_tokens = self._process_tokens(tokens=[row[CSVKey.SOURCE_PARAM],
                                                                        row[CSVKey.TARGET_PARAM]])
            link = self._create_trace_link(source_id=row[CSVKey.SOURCE_ID_PARAM], source_token=source_tokens,
                                           target_id=row[CSVKey.TARGET_ID_PARAM], target_token=target_tokens,
                                           label=row[CSVKey.LABEL_PARAM])
            links[link.id] = link
            self._add_to_link_ids(link, pos_link_ids, neg_link_ids)

        return TraceDataset(links=links, pos_link_ids=pos_link_ids, neg_link_ids=neg_link_ids)

    @staticmethod
    def _add_to_link_ids(link: TraceLink, pos_link_ids: List[int], neg_link_ids: List[int]) -> None:
        """
        Adds the trace link id to the pos_link_ids if true link else neg_link_ids
        :param link: the trace link to add to ids
        :param pos_link_ids: the list of current positive link ids
        :param neg_link_ids: the list of current negative link ids
        :return: None
        """
        if link.is_true_link:
            pos_link_ids.append(link.id)
        else:
            neg_link_ids.append(link.id)

    @staticmethod
    def _create_trace_link(source_id: str, source_token: str, target_id: str, target_token: str, label: int) -> TraceLink:
        """
        Generates a TraceLink object from the linked artifact information
        :param source_id: the id of the source artifact
        :param source_token: the content of the source artifact
        :param target_id: the id of the target artifact
        :param target_token: the content of the target artifact
        :param label: the label indicating if this is a true link
        :return: the trace link
        """
        source = Artifact(source_id, source_token)
        target = Artifact(target_id, target_token)
        is_true_link = label == 1
        return TraceLink(source, target, is_true_link)
