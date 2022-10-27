import os
from typing import List, Dict, Tuple, Set

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from tracer.dataset.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from tracer.dataset.creators.safa_dataset_creator import SafaDatasetCreator, SafaKeys
from tracer.dataset.trace_dataset import TraceDataset
from tracer.pre_processing.pre_processing_option import PreProcessingOption
from tracer.pre_processing.pre_processor import PreProcessor


class RepositoryKeys(SafaKeys):
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
    KEYS = RepositoryKeys()
    TRACE_FILE_2_ARTIFACTS = {RepositoryKeys.COMMIT2ISSUE_FILE_NAME: (RepositoryKeys.COMMIT_FILE_NAME, RepositoryKeys.ISSUE_FILE_NAME),
                              RepositoryKeys.PULL2ISSUE_FILE_NAME: (RepositoryKeys.PULL_FILE_NAME, RepositoryKeys.ISSUE_FILE_NAME)}

    def __init__(self, repo_paths: List[str], pre_processing_params: Tuple[List[PreProcessingOption], Dict] = None,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Responsible for creating a dataset from a repository
        :param repo_paths: list of paths to all repositories
        :param pre_processing_params: tuple containing the desired pre-processing steps and related params
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(pre_processing_params, use_linked_targets_only)
        self.repo_paths = repo_paths

    def create(self) -> TraceDataset:
        dataset = None
        for repo_path in self.repo_paths:
            repo_dataset = SafaDatasetCreator(repo_path, self.pre_processor, self.KEYS,
                                              self.TRACE_FILE_2_ARTIFACTS, self.use_linked_targets_only).create()

            dataset = dataset + repo_dataset if dataset else repo_dataset
        return dataset
