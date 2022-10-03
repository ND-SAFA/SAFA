import os
from typing import Dict, List, Tuple

import pandas as pd

from experiment.common.artifact_level import ArtifactLevel

GREADER_PATH = "/Users/albertorodriguez/Projects/SAFA/greader"
SAFA_PATH = os.path.join(GREADER_PATH, "safa")


class Project:
    def __init__(self, repo_name: str):
        self.repo_name = repo_name
        self.issues = self.__read_data_file("issue.csv")
        self.pulls = self.__read_data_file("pull.csv")
        self.commits = self.__read_data_file("commit.csv")
        self.commit2issue = self.__read_data_file("commit2issue.csv")
        self.pull2issue = self.__read_data_file("pull2issue.csv")

    def __read_data_file(self, data_file_name: str):
        return pd.read_csv(os.path.join(SAFA_PATH, self.repo_name, data_file_name))

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
            body_clean = Project.__clean_text(row["content"])
            if body_clean is not None:
                source[row["id"]] = body_clean
        return source

    @staticmethod
    def __get_links(links_df: pd.DataFrame) -> List[Tuple[str, str]]:
        links = []
        for i, link in links_df.iterrows():
            links.append((link["source"], link["target"]))
        return links

    @staticmethod
    def __clean_text(text: str):
        return text
