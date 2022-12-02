from typing import List

import pandas as pd

from data.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from data.formats.csv_format import CSVFormat
from data.datasets.trace_dataset import TraceDataset
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep


class CSVDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, data_file_path: str, data_cleaning_steps: List[AbstractDataProcessingStep] = None):
        """
        Constructs data in CSV format
        :param data_file_path: path to csv
        :param data_cleaning_steps: tuple containing the desired pre-processing steps and related params
        """
        super().__init__(data_cleaning_steps, use_linked_targets_only=False)
        self.data_file_path = data_file_path

    def create(self) -> TraceDataset:
        """
        Creates the data
        :return: the data
        """
        data_df = self._read_data_file(self.data_file_path)
        return self.create_from_dataframe(data_df)

    def create_from_dataframe(self, data_df: pd.DataFrame) -> TraceDataset:
        """
        Creates a trace dataset from a dataframe in the csv format
        :param data_df: the dataframe
        :return: TraceDataset
        """
        links = {}
        pos_link_ids, neg_link_ids = [], []
        for i, row in data_df.iterrows():
            source_tokens, target_tokens = self._process_tokens(tokens=[row[CSVFormat.SOURCE],
                                                                        row[CSVFormat.TARGET]])
            link = self._create_trace_link(source_id=row[CSVFormat.SOURCE_ID], source_token=source_tokens,
                                           target_id=row[CSVFormat.TARGET_ID], target_token=target_tokens,
                                           label=row[CSVFormat.LABEL])
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
    def _create_trace_link(source_id: str, source_token: str, target_id: str, target_token: str,
                           label: int) -> TraceLink:
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

    @staticmethod
    def _read_data_file(data_file_path: str) -> pd.DataFrame:
        """
        Reads the csv file and returns a dataframe containing the contents
        :param data_file_path: the path to the data file
        :return: a dataframe containing the contents
        """
        return pd.read_csv(data_file_path)
