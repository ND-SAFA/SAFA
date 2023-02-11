from abc import ABC, abstractmethod
from typing import Dict


class AbstractDatasetDescriptor(ABC):
    """
    Provides common interface for supported dataset.
    """

    @classmethod
    @abstractmethod
    def get_description(cls) -> str:
        """
        :return: Returns the description of the dataset being read.
        """

    @classmethod
    @abstractmethod
    def get_url(cls) -> str:
        """
        :return: Returns the url of the download file.
        """

    @classmethod
    @abstractmethod
    def get_citation(cls) -> str:
        """
        :return: Returns the citation information for this dataset.
        """

    @classmethod
    @abstractmethod
    def get_definition(cls) -> Dict:
        """
        :return: Returns project definition.
        """
