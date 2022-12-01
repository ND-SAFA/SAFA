from typing import Dict, List, Tuple

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from tracer.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from tracer.datasets.creators.safa_dataset_creator import SafaDatasetCreator
from tracer.datasets.formats.repository_format import RepositoryFormat
from tracer.datasets.formats.safa_format import SafaFormat
from tracer.datasets.trace_dataset import TraceDataset
from tracer.datasets.processing.cleaning.data_cleaning_steps import DataCleaningSteps


class RepositoryDatasetCreator(AbstractTraceDatasetCreator):
    KEYS = RepositoryFormat()

    def __init__(self, repo_paths: List[str], data_cleaning_steps: Tuple[List[DataCleaningSteps], Dict] = None,
                 data_keys: SafaFormat = KEYS, use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Responsible for creating a datasets from a repository
        :param repo_paths: list of paths to all repositories
        :param data_cleaning_steps: tuple containing the desired pre-processing steps and related params
        :param data_keys: keys to use to access data
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(data_cleaning_steps, use_linked_targets_only)
        self.repo_paths = repo_paths
        self.keys = data_keys
        self.data_cleaning_steps = data_cleaning_steps

    def create(self) -> TraceDataset:
        """
        Creates the datasets from the repository paths
        :return: the datasets
        """
        dataset = None
        for repo_path in self.repo_paths:
            repo_dataset = SafaDatasetCreator(repo_path, self.data_cleaning_steps, self.keys,
                                              self._use_linked_targets_only).create()

            dataset = dataset + repo_dataset if dataset else repo_dataset
        return dataset
