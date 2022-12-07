from typing import Dict, List, Tuple

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from data.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.creators.safa_dataset_creator import SafaDatasetCreator
from data.formats.repository_format import RepositoryFormat
from data.formats.safa_format import SafaFormat
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner


class RepositoryDatasetCreator(AbstractTraceDatasetCreator):
    KEYS = RepositoryFormat()

    def __init__(self, repo_paths: List[str], data_cleaner: DataCleaner = None,
                 data_keys: SafaFormat = KEYS, use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Responsible for creating a data from a repository
        :param repo_paths: list of paths to all repositories
        :param data_cleaner: the data cleaner to use on the data
        :param data_keys: keys to use to access data
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(data_cleaner, use_linked_targets_only)
        self.repo_paths = repo_paths
        self.keys = data_keys

    def create(self) -> TraceDataset:
        """
        Creates the data from the repository paths
        :return: the data
        """
        dataset = None
        for repo_path in self.repo_paths:
            repo_dataset = SafaDatasetCreator(repo_path, data_cleaner=self.data_cleaner, data_keys=self.keys,
                                              use_linked_targets_only=self._use_linked_targets_only).create()

            dataset = dataset + repo_dataset if dataset else repo_dataset
        return dataset
