from abc import ABC, abstractmethod
from typing import List
import pandas as pd

from gen_common.data.summarizer.artifacts_summarizer import ArtifactsSummarizer


class AbstractEntityFormat(ABC):
    """
    Defines interface for format responsible for converting data path into entities.
    """

    @classmethod
    def parse(cls, data_path: str, summarizer: ArtifactsSummarizer = None, **params) -> pd.DataFrame:
        """
        Parses a data into DataFrame of entities.
        :param data_path: The path to the data to parse
        :param summarizer: If provided, will summarize the artifact content
        :return: DataFrame of parsed entities.
        """
        return cls._parse(data_path, summarizer, **params)

    @classmethod
    @abstractmethod
    def _parse(cls, data_path: str, summarizer: ArtifactsSummarizer = None, **params) -> pd.DataFrame:
        """
        Parses a data into DataFrame of entities.
        :param data_path: The path to the data to parse
        :param summarizer: If provided, will summarize the artifact content
        :return: DataFrame of parsed entities.
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

    @staticmethod
    def performs_summarization() -> bool:
        """
        Returns whether the child format handles summarizations internally (see Folder entity Format)
        :return: If True, the child format handles summarizations internally, else should be handled in parent
        """
        return False
