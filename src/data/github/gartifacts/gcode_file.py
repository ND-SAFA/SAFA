import os
from typing import Callable, Dict, Union

from data.github.abstract_github_entity import AbstractGithubArtifact
from util.file_util import FileUtil
from util.override import overrides


class GCodeFile(AbstractGithubArtifact):
    """
    Represents a code artifact in a github repository.
    """

    def __init__(self, file_path: str, base_path: str):
        """
        Initialized code artifact targeting file at path.
        :param file_path: The path to the code file to parse.
        """
        self.file_path = file_path
        self.base_path = base_path
        self.content = FileUtil.read_file(self.file_path)

    @overrides(AbstractGithubArtifact)
    def as_dataframe_entry(self, **kwargs) -> Union[Dict, None]:
        """
        Exports state as dictionary.
        :param kwargs: Additional parameters for exporting artifact.
        :return:
        """
        return {"id": self.get_id(), "content": self.content}

    @overrides(AbstractGithubArtifact)
    def get_state_dict(self) -> Dict:
        """
        :return: Returns the state dictionary of the code artifact.
        """
        return {**self.as_dataframe_entry(), "file_path": self.file_path, "base_path": self.base_path}

    @staticmethod
    @overrides(AbstractGithubArtifact)
    def from_state_dict(state_dict: Dict) -> "GCodeFile":
        """
        Creates GCodeFile from state dictionary.
        :param state_dict: The state dictionary of github code artifact.
        :return: The constructed github code artifact.
        """
        return GCodeFile(state_dict["file_path"], state_dict["base_path"])

    @overrides(AbstractGithubArtifact)
    def get_id(self) -> str:
        """
        Returns the id of the artifact, its file path.
        :return: Path to code file.
        """
        return os.path.relpath(self.file_path, self.base_path)

    def clean_content(self, cleaner: Callable[[str], str]) -> None:
        """
        Cleans content of commit.
        :param cleaner: The cleaning function return cleaned string.
        :return: None
        """
        self.content = cleaner(self.content)
