import json
import os
from typing import List, Set

import pandas as pd

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from data.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.trace_dataset import TraceDataset
from data.formats.safa_format import SafaFormat
from data.processing.cleaning.data_cleaner import DataCleaner
from data.tree.artifact import Artifact


class SafaDatasetCreator(AbstractTraceDatasetCreator):
    JSON_EXT = ".json"
    CSV_EXT = ".csv"
    KEYS = SafaFormat()

    def __init__(self, project_path: str, data_cleaner: DataCleaner = None,
                 data_keys: SafaFormat = KEYS, use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Creates a data from the SAFA data format.
        :param project_path: the path to the project
        :param data_cleaner: the data cleaner to use on the data
        :param data_keys: keys to use to access data
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(data_cleaner, use_linked_targets_only)
        self.project_path = project_path
        self.keys = data_keys

    def create(self) -> TraceDataset:
        """
        Creates the data
        :return: the data
        """
        return self._create_dataset_from_files(self.keys)

    def _create_dataset_from_files(self, keys: SafaFormat) -> TraceDataset:
        """
        Creates data params from data files
        :param keys: keys used to access data in dataframe
        :return: the links, pos_link-ids, and neg_link_ids
        """
        links = {}
        pos_link_ids = set()
        for trace_file, source_target_files in keys.trace_files_2_artifacts.items():
            source_artifacts = self._create_artifacts_from_file(source_target_files[0])
            target_artifacts = self._create_artifacts_from_file(source_target_files[1])
            layer_pos_link_ids = self._get_pos_link_ids_from_file(trace_file)
            pos_link_ids = pos_link_ids.union(layer_pos_link_ids)
            links.update(self._create_links_for_layer(source_artifacts, target_artifacts, layer_pos_link_ids))
        neg_link_ids = set(links.keys()).difference(pos_link_ids)
        return TraceDataset(links, list(pos_link_ids), list(neg_link_ids))

    def _create_artifacts_from_file(self, data_file_name: str) -> List[Artifact]:
        """
        Create artifacts in artifact file.
        :param data_file_name: The name of the artifact file to read.
        :return: List of artifacts in file.
        """
        artifacts_file = self._read_data_file(self.project_path, data_file_name, self.keys.artifacts_key)

        artifacts = []
        for i, row in artifacts_file.iterrows():
            artifact_tokens = self._process_tokens(row[self.keys.artifact_token_key])
            if artifact_tokens:
                artifacts.append(Artifact(row[self.keys.artifact_id_key], artifact_tokens))

        return artifacts

    def _get_pos_link_ids_from_file(self, data_file_name: str) -> Set[int]:
        """
        Extracts positive trace links from trace files in project.
        :return: Trace link ids of positive links.
        """
        links_df = self._read_data_file(self.project_path, data_file_name, self.keys.traces_key)
        return self._get_pos_link_ids([(link[self.keys.source_id_key], link[self.keys.target_id_key])
                                       for _, link in links_df.iterrows()])

    @staticmethod
    def _read_data_file(project_path: str, data_file_name: str, data_key: str) -> pd.DataFrame:
        """
        Returns file content as dataframe.
        :param project_path: Path to project dir
        :param data_file_name: name of the data file
        :param data_key: used to access the list of dictionaries in a json file
        :return: dataframe containing file content.
        """
        ext = os.path.splitext(data_file_name)[-1]
        if ext == SafaDatasetCreator.JSON_EXT:
            data_read_method = SafaDatasetCreator._read_json_file
        elif ext == SafaDatasetCreator.CSV_EXT:
            data_read_method = SafaDatasetCreator._read_csv_file
        else:
            raise Exception("Unknown file type %s" % ext)

        return data_read_method(project_path, data_file_name, data_key)

    @staticmethod
    def _read_json_file(project_path: str, data_file_name: str, data_key: str) -> pd.DataFrame:
        """
        Returns JSON file content as dataframe.
        :param project_path: Path to project dir
        :param data_file_name: name of the data file
        :param data_key: used to access the list of dictionaries in a json file
        :return: dataframe containing file content.
        """
        path_to_file = os.path.join(project_path, data_file_name)
        with open(path_to_file, "r") as json_file:
            json_content = json.loads(json_file.read())
        return pd.json_normalize(json_content[data_key])

    @staticmethod
    def _read_csv_file(project_path: str, data_file_name: str, data_key: str = ''):
        """
        Returns CSV file content as dataframe.
        :param project_path: Path to project dir
        :param data_file_name: name of the data file
        :param data_key: the key to access data within the file (not used)
        :return: dataframe containing file content.
        """
        return pd.read_csv(os.path.join(project_path, data_file_name))
