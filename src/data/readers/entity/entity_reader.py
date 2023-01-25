import os
from typing import Dict, Generic, Optional, TypeVar

import pandas as pd

from data.readers.entity.supported_entity_formats import SupportedEntityFormats
from data.keys.structure_keys import StructuredKeys
from util.dataframe_util import DataFrameUtil
from util.json_util import JsonUtil

EntityType = TypeVar("EntityType")


class EntityReader(Generic[EntityType]):
    """
    Responsible for converting data into entities.
    """

    def __init__(self, base_path: str, definition: Dict, conversions: Dict = None):
        """
        Creates entity reader for project at base_path using definition given.
        :param base_path: The base path to find data.
        :param definition: Defines how to parse the data.
        :param conversions: The definitions to the data to standardize it.
        """
        required_properties = [StructuredKeys.PATH]
        JsonUtil.require_properties(definition, required_properties)
        self.definition: Dict = definition
        self.path = os.path.join(base_path, JsonUtil.get_property(definition, StructuredKeys.PATH))
        self.conversions: Dict[str, Dict] = conversions if conversions else None
        self.entity_type = None

    def read_entities(self) -> pd.DataFrame:
        """
        Reads original entities and applies any column conversion defined in definition.
        :return: DataFrame containing processed entities.
        """
        source_entities_df = self.read_original_entities()
        column_conversion = self.get_column_conversion()
        processed_df = DataFrameUtil.rename_columns(source_entities_df, column_conversion)
        return processed_df

    def read_original_entities(self) -> pd.DataFrame:
        """
        Reads data and aggregates examples into data frame.
        :return: DataFrame containing original examples
        """
        parser_params = JsonUtil.get_property(self.definition, StructuredKeys.PARAMS, {})
        parser = SupportedEntityFormats.get_parser(self.path, self.definition)
        return parser(self.path, **parser_params)

    def get_column_conversion(self) -> Optional[Dict]:
        """
        Reads the column conversion to apply to given source entities.
        :return: Dictionary containing mapping from original column names to target ones.
        """
        if StructuredKeys.COLS in self.definition:
            conversion_id = JsonUtil.get_property(self.definition, StructuredKeys.COLS)
            assert self.conversions is not None, f"Could not find conversion {conversion_id} because none defined."
            return self.conversions[conversion_id]
        return None
