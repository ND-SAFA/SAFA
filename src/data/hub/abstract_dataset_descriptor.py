from abc import ABC, abstractmethod
from typing import Dict


class AbstractDatasetDescriptor(ABC):
    """
    Provides common interface for supported dataset.
    """

    @classmethod
    @abstractmethod
    def get_url(cls) -> str:
        """
        :return: Returns the url of the download file.
        """

    @classmethod
    @abstractmethod
    def get_definition(cls) -> Dict:
        """
        :return: Returns project definition.
        """
