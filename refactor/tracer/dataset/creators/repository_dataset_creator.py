import os
from collections import namedtuple
from typing import List, Dict, Tuple

from config.constants import USE_LINKED_TARGETS_ONLY_DEFAULT
from tracer.dataset.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from tracer.dataset.data_objects.artifact import Artifact
from tracer.dataset.data_objects.repository import Repository
from tracer.pre_processing.pre_processor import PreProcessor
import pandas as pd


class RepositoryDatasetCreator(AbstractTraceDatasetCreator):
    def __init__(self, repo_paths: List[str], pre_processor: PreProcessor,
                 use_linked_targets_only: bool = USE_LINKED_TARGETS_ONLY_DEFAULT):
        self.repo_paths = repo_paths
        super().__init__(pre_processor, use_linked_targets_only)

    def get_levels(self, repository: Repository) -> List[namedtuple]:
        Level = namedtuple("Level", ["source_artifacts", "target_artifacts", "links"])
        return [
            Level(
                self._create_artifacts_from_data(repository.commits),
                self._create_artifacts_from_data(repository.issues),
                self._get_links(repository.commit2issue)),
            Level(
                self._create_artifacts_from_data(repository.pulls),
                self._create_artifacts_from_data(repository.issues),
                self._get_links(repository.pull2issue))
        ]

    def _create_artifacts_from_data(self, artifacts_data: pd.DataFrame) -> List[Artifact]:
        artifacts = []
        for i, row in artifacts_data.iterrows():
            body_clean = self._process_tokens(row[Repository.CONTENT_PARAM])
            if body_clean is not None:
                artifacts.append(Artifact(row[Repository.ID_PARAM], body_clean))
        return artifacts

    @staticmethod
    def _get_links(links_df: pd.DataFrame) -> List[Tuple[str, str]]:
        links = []
        for i, link in links_df.iterrows():
            links.append((link[Repository.SOURCE_PARAM], link[Repository.TARGET_PARAM]))
        return links

    def __create_training_data(self):
        training_sources = []
        training_targets = []
        training_links = []
        for repo_path in self.repo_paths:
            repository = Repository(repo_path)
            for level in repository.get_levels():
                training_sources.append(level.source_artifacts)
                training_targets.append(level.target_artifacts)
                training_links.extend(level.links)

        return training_sources, training_targets, training_links
