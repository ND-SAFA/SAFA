from typing import Dict, Tuple

import pandas as pd

from data.hub.trace_dataset_downloader import TraceDatasetDownloader
from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.structured_project_reader import StructuredProjectReader


class HubProjectReader(AbstractProjectReader):
    """
    Reads a supported project.
    """

    def __init__(self, name: str, **kwargs):
        """
        Initializes reader for supported project.
        :param name: Name of supported project.
        """
        self.project_name = name
        self.kwargs = kwargs
        self.project_reader = None

    def read_project(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        :return: Reads the dataframes of the project.
        """
        downloader = TraceDatasetDownloader(self.project_name)
        project_path = downloader.download()
        self.project_reader = StructuredProjectReader(project_path, **self.kwargs)
        return self.project_reader.read_project()

    def get_project_name(self) -> str:
        """
        :return: Returns the name of the project being read.
        """
        return self.project_name

    def get_overrides(self) -> Dict:
        """
        :return: Returns the overrides of the project reader.
        """
        return self.project_reader.get_overrides()
