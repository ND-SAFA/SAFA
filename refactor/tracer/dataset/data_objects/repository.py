import os
from collections import namedtuple
from typing import Dict, List, Tuple

import pandas as pd


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