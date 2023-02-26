import os.path
from typing import Dict, Tuple

import pandas as pd

from data.hub.abstract_hub_id import AbstractHubId
from data.hub.supported_datasets import SupportedDatasets
from data.hub.trace_dataset_downloader import TraceDatasetDownloader
from data.readers.abstract_project_reader import AbstractProjectReader


class HubProjectReader(AbstractProjectReader):
    """
    Reads a supported project.
    """

    def __init__(self, name: str, id_kwargs: dict = None, **kwargs):
        """
        Initializes reader for supported project.
        :param name: Name of supported project.
        :param kwargs: Additional parameters passed to project identifiers.
        """
        if id_kwargs is None:
            id_kwargs = {}
        super().__init__()
        self.project_name = name
        self.id_kwargs = id_kwargs
        self.kwargs = kwargs
        self.project_reader = None

    def read_project(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        :return: Reads the dataframes of the project.
        """
        descriptor: AbstractHubId = SupportedDatasets.get_value(self.project_name)(**self.id_kwargs)
        downloader = TraceDatasetDownloader(descriptor)
        data_dir = downloader.download()
        project_reader_class = descriptor.get_project_reader()
        project_definition_path = descriptor.get_definition_path(data_dir)
        project_path = os.path.split(project_definition_path)[0]
        self.project_reader = project_reader_class(project_path, **self.kwargs)
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
