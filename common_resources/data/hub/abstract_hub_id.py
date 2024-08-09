from abc import ABC, abstractmethod
from typing import Type

from common_resources.data.readers.abstract_project_reader import AbstractProjectReader
from common_resources.data.readers.structured_project_reader import StructuredProjectReader


class AbstractHubId(ABC):
    """
    Interface for definition where to download a dataset and how to read it.
    """

    def __init__(self, local_path: str = None):
        """
        Initializes dataset to defined url or local path.
        :param local_path: The path to local version of the dataset.
        """
        self.local_path = local_path

    def get_path(self) -> str:
        """
        Returns path to dataset.
        :return: Local path if defined otherwise hub url.
        """
        if self.local_path:
            return self.local_path
        return self.get_url()

    def get_project_path(self, data_dir: str) -> str:
        """
        :param data_dir: Path to directory containing project data.
        :return: Returns the path to save and read definition from.
        """
        return data_dir

    @abstractmethod
    def get_url(self) -> str:
        """
        :return: The url of the file(s) to download.
        """

    @staticmethod
    def get_project_reader() -> Type[AbstractProjectReader]:
        """
        :return: Returns the project reader for hub project.s
        """
        return StructuredProjectReader
