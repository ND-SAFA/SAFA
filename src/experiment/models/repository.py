import os
from typing import Dict, List, Tuple

import pandas as pd

from experiment.models.artifact_level import ArtifactLevel


class Repository:
    """
    Represents a GitHub repository with its trace links mined using GREADER.
    """
    ISSUE_FILE_NAME = "issue.csv"
    PULL_FILE_NAME = "pull.csv"
    COMMIT_FILE_NAME = "commit.csv"
    COMMIT2ISSUE_FILE_NAME = "commit2issue.csv"
    PULL2ISSUE_FILE_NAME = "pull2issue.csv"
    CONTENT_PARAM = "content"
    ID_PARAM = "id"
    SOURCE_PARAM = "source"
    TARGET_PARAM = "target"

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.issues = self.__read_data_file(self.ISSUE_FILE_NAME)
        self.pulls = self.__read_data_file(self.PULL_FILE_NAME)
        self.commits = self.__read_data_file(self.COMMIT_FILE_NAME)
        self.commit2issue = self.__read_data_file(self.COMMIT2ISSUE_FILE_NAME)
        self.pull2issue = self.__read_data_file(self.PULL2ISSUE_FILE_NAME)

    def __read_data_file(self, data_file_name: str):
        return pd.read_csv(os.path.join(self.repo_path, data_file_name))

    def get_levels(self) -> List[ArtifactLevel]:
        return [
            ArtifactLevel(
                self.__get_artifact_dict(self.commits),
                self.__get_artifact_dict(self.issues),
                self.__get_links(self.commit2issue)),
            ArtifactLevel(
                self.__get_artifact_dict(self.pulls),
                self.__get_artifact_dict(self.issues),
                self.__get_links(self.pull2issue))
        ]

    def get_sources(self) -> List[Dict[str, str]]:
        return self.get_artifact_dicts([self.commits, self.pulls])

    def get_targets(self) -> List[Dict[str, str]]:
        return self.get_artifact_dicts([self.issues, self.issues])

    def get_artifact_dicts(self, data_files: List[pd.DataFrame]) -> List[Dict[str, str]]:
        return [self.__get_artifact_dict(artifact) for artifact in data_files]

    @staticmethod
    def __get_artifact_dict(artifacts: pd.DataFrame) -> Dict[str, str]:
        source = {}
        for i, row in artifacts.iterrows():
            body_clean = Repository.__clean_text(row[Repository.CONTENT_PARAM])
            if body_clean is not None:
                source[row[Repository.ID_PARAM]] = body_clean
        return source

    @staticmethod
    def __get_links(links_df: pd.DataFrame) -> List[Tuple[str, str]]:
        links = []
        for i, link in links_df.iterrows():
            links.append((link[Repository.SOURCE_PARAM], link[Repository.TARGET_PARAM]))
        return links

    @staticmethod
    def __clean_text(text: str):
        return text
