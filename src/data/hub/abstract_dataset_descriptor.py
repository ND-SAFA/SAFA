from abc import ABC, abstractmethod
from typing import Dict


class AbstractDatasetDescriptor(ABC):
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
