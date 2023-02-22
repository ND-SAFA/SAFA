from abc import ABC, abstractmethod
from typing import Dict, Type

from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.structured_project_reader import StructuredProjectReader


class AbstractHubId(ABC):
    """
    Interface for definition where to download a dataset and how to read it.
    """

    @classmethod
    @abstractmethod
    def get_url(cls) -> str:
        """
        :return: The url of the file(s) to download.
        """

    @classmethod
    @abstractmethod
    def get_definition(cls) -> Dict:
        """
        :return: Returns project definition for structured project reader.
        """

    @staticmethod
    def get_project_reader() -> Type[AbstractProjectReader]:
        """
        :return: Returns the project reader for hub project.s
        """
        return StructuredProjectReader
