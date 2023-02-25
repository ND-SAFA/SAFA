import os
from abc import ABC, abstractmethod
from typing import Dict, Type

from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.definitions.structure_project_definition import StructureProjectDefinition
from data.readers.structured_project_reader import StructuredProjectReader
from util.file_util import FileUtil


class AbstractHubId(ABC):
    """
    Interface for definition where to download a dataset and how to read it.
    """

    @abstractmethod
    def get_url(self) -> str:
        """
        :return: The url of the file(s) to download.
        """

    @abstractmethod
    def get_definition(self) -> Dict:
        """
        :return: Returns project definition for structured project reader.
        """

    def get_definition_path(self, data_dir: str) -> str:
        """
        :return: Returns the path to save and read definition from.
        """
        zip_file_query = FileUtil.ls_dir(data_dir, ignore=["__MACOSX"])
        assert len(zip_file_query) == 1, f"Found more than one folder for extracted files:{zip_file_query}"
        project_dir_path = zip_file_query[0]  # include path to directory
        return os.path.join(project_dir_path, StructureProjectDefinition.STRUCTURE_DEFINITION_FILE_NAME)

    @staticmethod
    def get_project_reader() -> Type[AbstractProjectReader]:
        """
        :return: Returns the project reader for hub project.s
        """
        return StructuredProjectReader
