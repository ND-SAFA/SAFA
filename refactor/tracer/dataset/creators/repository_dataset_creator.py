from typing import Dict, List, Tuple

from constants.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from tracer.dataset.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from tracer.dataset.creators.safa_dataset_creator import SafaDatasetCreator, SafaKeys
from tracer.dataset.trace_dataset import TraceDataset
from tracer.pre_processing.pre_processing_option import PreProcessingOption


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
    TRACE_FILE_2_ARTIFACTS = {COMMIT2ISSUE_FILE_NAME: (COMMIT_FILE_NAME, ISSUE_FILE_NAME),
                              PULL2ISSUE_FILE_NAME: (PULL_FILE_NAME, ISSUE_FILE_NAME)}

    def __init__(self, artifact_id_key: str = ARTIFACT_ID, artifact_token_key: str = ARTIFACT_TOKEN,
                 source_id_key: str = SOURCE_ID,
                 target_id_key: str = TARGET_ID, artifacts_key: str = '', traces_key: str = '',
                 trace_files_2_artifacts: Dict[str, Tuple[str, str]] = None):
        super().__init__(artifact_id_key, artifact_token_key, source_id_key, target_id_key, artifacts_key, traces_key,
                         trace_files_2_artifacts=trace_files_2_artifacts if trace_files_2_artifacts else
                         RepositoryKeys.TRACE_FILE_2_ARTIFACTS)


class RepositoryDatasetCreator(AbstractTraceDatasetCreator):
    KEYS = RepositoryKeys()

    def __init__(self, repo_paths: List[str], pre_processing_params: Tuple[List[PreProcessingOption], Dict] = None,
                 data_keys: SafaKeys = KEYS, use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        """
        Responsible for creating a dataset from a repository
        :param repo_paths: list of paths to all repositories
        :param pre_processing_params: tuple containing the desired pre-processing steps and related params
        :param data_keys: keys to use to access data
        :param use_linked_targets_only: if True, uses only the targets that make up at least one true link
        """
        super().__init__(pre_processing_params, use_linked_targets_only)
        self.repo_paths = repo_paths
        self.keys = data_keys
        self.pre_processing_params = pre_processing_params

    def create(self) -> TraceDataset:
        """
        Creates the dataset from the repository paths
        :return: the dataset
        """
        dataset = None
        for repo_path in self.repo_paths:
            repo_dataset = SafaDatasetCreator(repo_path, self.pre_processing_params, self.keys,
                                              self.use_linked_targets_only).create()

            dataset = dataset + repo_dataset if dataset else repo_dataset
        return dataset
