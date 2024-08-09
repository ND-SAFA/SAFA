import os
from typing import Dict, Generic, Optional, Tuple, TypeVar

import pandas as pd

from common_resources.tools.util.dataframe_util import DataFrameUtil
from common_resources.tools.util.json_util import JsonUtil
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.data.keys.structure_keys import StructuredKeys
from common_resources.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from common_resources.data.readers.entity.supported_entity_formats import SupportedEntityFormats
from common_resources.data.summarizer.artifacts_summarizer import ArtifactsSummarizer

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
            assert self.conversions is not None, f"Could not find conversion {conversion_id} because none defined."
            return self.conversions[conversion_id]
        return None
