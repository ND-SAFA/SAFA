import os
from typing import List, Dict, Tuple, Set

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from tracer.dataset.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator, Keys
from tracer.dataset.trace_dataset import TraceDataset
from tracer.pre_processing.pre_processor import PreProcessor
import pandas as pd


class RepositoryKeys(Keys):
    ISSUE_FILE_NAME = "issue.csv"
    PULL_FILE_NAME = "pull.csv"
    COMMIT_FILE_NAME = "commit.csv"
    COMMIT2ISSUE_FILE_NAME = "commit2issue.csv"
    PULL2ISSUE_FILE_NAME = "pull2issue.csv"
    ARTIFACT_TOKEN = "content"
    ARTIFACT_ID = "id"
    SOURCE_ID = "source"
    TARGET_ID = "target"

    def __init__(self):
        super().__init__(RepositoryKeys.ARTIFACT_ID, RepositoryKeys.ARTIFACT_TOKEN, RepositoryKeys.SOURCE_ID, RepositoryKeys.TARGET_ID)


class RepositoryDatasetCreator(AbstractTraceDatasetCreator):
    TRACE_FILE_2_ARTIFACTS = {RepositoryKeys.COMMIT2ISSUE_FILE_NAME: (RepositoryKeys.COMMIT_FILE_NAME, RepositoryKeys.ISSUE_FILE_NAME),
                              RepositoryKeys.PULL2ISSUE_FILE_NAME: (RepositoryKeys.PULL_FILE_NAME, RepositoryKeys.ISSUE_FILE_NAME)}

    def __init__(self, repo_paths: List[str], pre_processor: PreProcessor,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        self.repo_paths = repo_paths
        super().__init__(pre_processor, use_linked_targets_only)

    def create(self) -> TraceDataset:
        """
        Creates the dataset
        :return: the dataset
        """
        links = {}
        pos_link_ids, neg_link_ids = set(), set()
        for repo_path in self.repo_paths:
            repo_links, repo_pos_link_ids, repo_neg_link_ids = self._create_dataset_params_from_files(RepositoryKeys(),
                                                                                                      repo_path,
                                                                                                      self.TRACE_FILE_2_ARTIFACTS)
            links.update(repo_links)
            pos_link_ids.add(repo_pos_link_ids)
            neg_link_ids.add(repo_neg_link_ids)
        return TraceDataset(links, list(pos_link_ids), list(neg_link_ids))

    @staticmethod
    def _read_data_file(project_path: str, data_file_name: str, data_key: str = ''):
        """
        Returns CSV file content as dataframe.
        :param project_path: Path to project dir
        :param data_file_name: name of the data file
        :param data_key: the key to access data within the file (not used)
        :return: dataframe containing file content.
        """
        return pd.read_csv(os.path.join(project_path, data_file_name))
