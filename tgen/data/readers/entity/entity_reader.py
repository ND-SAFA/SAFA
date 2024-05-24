import os
from typing import Dict, Generic, Optional, Tuple, TypeVar

import pandas as pd

from tgen.common.logging.logger_manager import logger
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.json_util import JsonUtil
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from tgen.data.readers.entity.supported_entity_formats import SupportedEntityFormats
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer

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
        JsonUtil.require_properties(definition, [StructuredKeys.PATH])
        self.definition: Dict = definition
        self.path = os.path.join(base_path, JsonUtil.get_property(definition, StructuredKeys.PATH))
        self.conversions: Dict[str, Dict] = conversions
        self.entity_type = None

    def read_entities(self, summarizer: ArtifactsSummarizer = None) -> pd.DataFrame:
        """
        Reads original entities and applies any column conversion defined in definition.
        :param summarizer: The summarizer to use if summarizing right after reding entities.
        :return: DataFrame containing processed entities.
        """
        parser, parser_params = self.get_parser()
        source_entities_df = parser.parse(self.path, summarizer=summarizer, **parser_params)
        column_conversion = self.get_column_conversion()
        processed_df = DataFrameUtil.rename_columns(source_entities_df, column_conversion)
        logger.info(f"{self.path}:{len(source_entities_df)}")
        return processed_df

    def get_parser(self) -> Tuple[AbstractEntityFormat, Dict]:
        """
        Reads data and aggregates examples into data frame.
        :return: DataFrame containing original examples
        """
        parser_params: Dict = JsonUtil.get_property(self.definition, StructuredKeys.PARAMS, {})
        parser = SupportedEntityFormats.get_parser(self.path, self.definition)
        return parser, parser_params

    def get_column_conversion(self) -> Optional[Dict]:
        """
        Reads the column conversion to apply to given source entities.
        :return: Dictionary containing mapping from original column names to target ones.
        """
        if StructuredKeys.COLS in self.definition:
            conversion_id = JsonUtil.get_property(self.definition, StructuredKeys.COLS)
            if not isinstance(conversion_id, str):
                raise Exception("`cols` property should be string referencing name of conversion defined in `conversions`.")
            if self.conversions is None or len(self.conversions) == 0:
                raise Exception(
                    "Column conversion referenced but not defined.\n\nMake sure `conversions` is defined in project file.")
            valid_conversions = list(self.conversions.keys())
            if conversion_id not in self.conversions:
                raise Exception(f"Could not find conversion {conversion_id}. Did you mean {valid_conversions}?")
            return self.conversions[conversion_id]
        return None
