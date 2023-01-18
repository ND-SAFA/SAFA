from typing import List

import pandas as pd

from data.datasets.creators.readers.entity.entity_parser_type import EntityParserType
from data.datasets.creators.readers.entity.formats.abstract_entity_format import AbstractEntityFormat


class XmlEntityFormat(AbstractEntityFormat):
    """
    Defines format for reading XML files into DataFrames.
    """

    @staticmethod
    def get_parser() -> EntityParserType:
        """
        :return: Returns pandas function for reading xml files into data frames.
        """
        return pd.read_xml

    @staticmethod
    def get_file_extensions() -> List[str]:
        """
        :return: Returns single xml format.
        """
        return [".xml"]
