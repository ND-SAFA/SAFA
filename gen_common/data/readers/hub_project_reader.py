from typing import Dict, Tuple

import pandas as pd

from gen_common.data.hub.abstract_hub_id import AbstractHubId
from gen_common.data.hub.supported_datasets import SupportedDatasets
from gen_common.data.hub.trace_dataset_downloader import TraceDatasetDownloader
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader


class HubProjectReader(AbstractProjectReader):
    """
    Reads a supported project.
    """

    def __init__(self, name: str, **kwargs):
        """
        Initializes reader for supported project.
        :param name: Name of supported project.
        :param kwargs: Additional parameters passed to project identifiers.
        """
        super().__init__()
        self.project_name = name
        self.kwargs = kwargs
        self.project_reader = None

    def read_project(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        :return: Reads the dataframes of the project.
        """
        descriptor: AbstractHubId = SupportedDatasets.get_value(self.project_name)(**self.kwargs)
        downloader = TraceDatasetDownloader(descriptor)
        data_dir = downloader.download()
        project_reader_class = descriptor.get_project_reader()
        project_path = descriptor.get_project_path(data_dir)
        self.project_reader = project_reader_class(project_path)
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

    def should_generate_negative_links(self) -> bool:
        """
       :return: Returns whether negative links should be implied by comparing artifacts.
       """
        return self.project_reader.should_generate_negative_links()
