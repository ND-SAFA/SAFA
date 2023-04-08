import os

import pandas as pd

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.util.file_util import FileUtil
from tgen.util.json_util import JsonUtil


class PromptProjectReader(AbstractProjectReader[PromptDataFrame]):
    """
    Responsible for reading artifacts and trace links and constructing
    a trace dataset.
    """

    FILE_EXT = ".jsonl"

    def __init__(self, project_path: str):
        """
        Creates reader for project at path and column definitions given.
        :param project_path: Path to the project.
        """
        super().__init__()
        assert FileUtil.get_file_ext(project_path) == self.FILE_EXT, f"Expected project path to be a {self.FILE_EXT} file"
        self.project_path = project_path

    def read_project(self) -> PromptDataFrame:
        """
        Reads project data from files.
        :return: Returns the data frames containing the project artifacts.
        """
        return PromptDataFrame(JsonUtil.read_jsonl_file(self.project_path))

    def get_project_name(self) -> str:
        """
        Gets the name of the project being read.
        :return:  Returns the name of the project being read.
        """
        return FileUtil.get_file_name(self.project_path)
