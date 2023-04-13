from typing import List

import pandas as pd

from tgen.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from tgen.data.summarizer.summarizer import Summarizer


class XmlEntityFormat(AbstractEntityFormat):
    """
    Defines format for reading XML files into DataFrames.
    """

    @classmethod
    def _parse(cls, data_path: str, summarizer: Summarizer = None, **params) -> pd.DataFrame:
        """
        Parses a XML file into DataFrame of entities.
        :param data_path: The path to the data to parse
        :param summarizer: If provided, will summarize the artifact content
        :return: DataFrame of parsed entities.
        """
        return pd.read_xml(data_path)

    @staticmethod
    def get_file_extensions() -> List[str]:
        """
        :return: Returns single xml format.
        """
        return [".xml"]
