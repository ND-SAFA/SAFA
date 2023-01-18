from typing import List

import pandas as pd

from data.datasets.creators.readers.entity.entity_parser_type import EntityParserType
from data.datasets.creators.readers.entity.formats.abstract_entity_format import AbstractEntityFormat


class CsvEntityFormat(AbstractEntityFormat):
    """
    Defines format for reading CSV files as entitites.
    """

    @staticmethod
    def get_parser() -> EntityParserType:
        """
        :return: Returns pandas data frame parser from csv files.
        """
        return pd.read_csv

    @staticmethod
    def get_file_extensions() -> List[str]:
        """
        :return: Returns single CSV format.
        """
        return [".csv", ".txt"]
