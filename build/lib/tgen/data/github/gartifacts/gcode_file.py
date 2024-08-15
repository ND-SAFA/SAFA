import os
from typing import Callable, Dict, Iterable, Set, Union

from common_resources.tools.constants.code_extensions import ALLOWED_CODE_EXTENSIONS

from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.override import overrides
from tgen.data.github.abstract_github_entity import AbstractGithubArtifact


class GCodeFile(AbstractGithubArtifact):
    """
    Represents a code artifact in a github repository.
    """

    def __init__(self, file_path: str, base_path: str):
        """
        Initialized code artifact targeting file at path.
        :param file_path: The path to the code file to parse.
        :param base_path: The base path of the project.
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

    @staticmethod
    def ends_with_allowed_code_ext(filename: str, allowed_code_ext: Set[str]) -> bool:
        """
        Determine if file has allowed extensions.
        :param filename: The file to check if it ends with an appropriate code ext
        :param allowed_code_ext: A list of allowed code ext
        :return: True if contains allowed extension else False.
        """
        for code_ext in allowed_code_ext:
            if filename.endswith(code_ext):
                return True
        return False

    @staticmethod
    def get_all_code_files_with_ext(dir_path: str, allowed_code_ext: Iterable[str] = None):
        """
        Reads all code files in directory with allowed extensions.
        :param dir_path: The path to the directory containing the code files
        :param allowed_code_ext: A list of allowed code ext
        :return: List containing all code file paths.
        """
        allowed_code_ext = ALLOWED_CODE_EXTENSIONS if allowed_code_ext is None else allowed_code_ext
        return FileUtil.get_all_paths(dir_path,
                                      lambda f: GCodeFile.ends_with_allowed_code_ext(f, allowed_code_ext))
