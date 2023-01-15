from typing import List

from data.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.creators.readers.project.repository_project_reader import RepositoryProjectReader
from data.datasets.keys.safa_format import SafaKeys
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner


class RepositoryDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, repo_paths: List[str], data_cleaner: DataCleaner = None,
                 data_keys: SafaKeys = SafaKeys):
        """
        Responsible for creating a data from a repository
        :param repo_paths: list of paths to all repositories
        :param data_cleaner: The cleaner responsible for processing artifact tokens.
        :param data_keys: keys to use to access data
        """
        super().__init__(data_cleaner)
        self.repo_paths = repo_paths
        self.data_keys = data_keys

    def create(self) -> TraceDataset:
        """
        Creates the data from the repository paths
        :return: the data
        """
        dataset = None
        for repo_path in self.repo_paths:
            repository_project_reader = RepositoryProjectReader(repo_path)
            repo_dataset = repository_project_reader.create()
            dataset = dataset + repo_dataset if dataset else repo_dataset
        return dataset
