from abc import ABC, abstractmethod
from typing import List

from data.readers.entity.entity_parser_type import EntityParserType


class AbstractEntityFormat(ABC):
    """
    Defines interface for format responsible for converting data path into entities.
    """

    @staticmethod
    @abstractmethod
    def get_parser() -> EntityParserType:
        """
        :return: Returns parser for reading data path into DataFrame of entities.
        """

    @staticmethod
    @abstractmethod
    def get_file_extensions() -> List[str]:
        """
        :return: Returns list of file extensions associated with format.
        """

    @classmethod
    def is_format(cls, data_path: str) -> bool:
        """
        Returns whether path is associated with format.
        :param data_path: The path to check if extension contained within it.
        :return: Whether path contains an extension associated with format.
        """

        for extension in cls.get_file_extensions():
            if extension in data_path:
                return True
        return False
