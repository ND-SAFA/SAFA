from typing import List

import pandas as pd

from gen_common.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from gen_common.data.summarizer.artifacts_summarizer import ArtifactsSummarizer
from gen_common.util.json_util import JsonUtil


class JsonEntityFormat(AbstractEntityFormat):
    """
    Defines format for reading entities from json files.
    """

    @classmethod
    def _parse(cls, data_path: str, summarizer: ArtifactsSummarizer = None, **params) -> pd.DataFrame:
        """
        Parses a JSON file into DataFrame of entities.
        :param data_path: The path to the data to parse
        :param summarizer: If provided, will summarize the artifact content
        :return: DataFrame of parsed entities.
        """
        return JsonEntityFormat.read_json(data_path, **params)

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
        :param entity_prop_name: The name of the property containing entities in json file. If none, dictionary is assumed to contain
        single property
        :return: DataFrame containing entities defined in JSON file.
        """
        data = JsonUtil.read_json_file(json_file_path)
        if entity_prop_name is None:
            keys = list(data.keys())
            assert len(keys) == 1, f"Unable to imply entity property name in JSON, found multiple: {keys}."
            entity_prop_name = keys[0]
        return pd.DataFrame(data[entity_prop_name])
