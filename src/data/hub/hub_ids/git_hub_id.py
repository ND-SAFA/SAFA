import os
from typing import Type

from data.hub.abstract_hub_id import AbstractHubId
from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.csv_project_reader import CsvProjectReader


class GitHubId(AbstractHubId):
    """
    Identifies the dataset containing slice of git links from Jinfeng's crawl.
    """

    def get_url(self) -> str:
        """
        :return: Returns URL to hub dataset.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/open-source/git.zip"

    @staticmethod
    def get_project_reader() -> Type[AbstractProjectReader]:
        """
        :return: Returns CSV project reader
        """
        return CsvProjectReader

    def get_project_path(self, data_dir: str) -> str:
        """
        Creates project path to CSV file to read.
        :param data_dir: Directory containing downloaded contents.
        :return: Path to CSV file.
        """
        return os.path.join(data_dir, "git.csv")
