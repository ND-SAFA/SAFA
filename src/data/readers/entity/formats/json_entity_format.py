from typing import List

import pandas as pd

from data.readers.entity.entity_parser_type import EntityParserType
from data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from util.file_util import FileUtil


class JsonEntityFormat(AbstractEntityFormat):
    """
    Defines format for reading entities from json files.
    """

    @classmethod
    def get_parser(cls) -> EntityParserType:
        """
        :return: Return custom method for reading json files as entities using an entity name.
        """
        return cls.read_json

    @staticmethod
    def get_file_extensions() -> List[str]:
        """
        :return: Return single JSON extension.
        """
        return [".json"]

    @staticmethod
    def read_json(json_file_path: str, entity_prop_name: str = None) -> pd.DataFrame:
        """
        Reads json file and construct data frame with entities.
        :param json_file_path: The path to the json file.
        :param entity_prop_name: The name of the property containing entities in json file. If none, dictionary is assumed to contain single property
        :return: DataFrame containing entities defined in JSON file.
        """
        data = FileUtil.read_json_file(json_file_path)
        if entity_prop_name is None:
            keys = list(data.keys())
            assert len(keys) == 1, f"Unable to imply entity property name in JSON, found multiple: {keys}."
            entity_prop_name = keys[0]
        return pd.DataFrame(data[entity_prop_name])
