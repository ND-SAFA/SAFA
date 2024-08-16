from typing import List

import pandas as pd

from gen_common.data.readers.entity.formats.abstract_entity_format import AbstractEntityFormat
from gen_common.data.summarizer.artifacts_summarizer import ArtifactsSummarizer


class CsvEntityFormat(AbstractEntityFormat):
    """
    Defines format for reading CSV files as entities.
    """

    @classmethod
    def _parse(cls, data_path: str, summarizer: ArtifactsSummarizer = None, **kwargs) -> pd.DataFrame:
        """
        Parses a CSV into DataFrame of entities.
        :param data_path: The path to the data to parse
        :param summarizer: If provided, will summarize the artifact content
        :return: DataFrame of parsed entities.
        """
        return pd.read_csv(data_path, **kwargs)

    @staticmethod
    def get_file_extensions() -> List[str]:
        """
        :return: Returns single CSV format.
        """
        return [".csv", ".txt"]
