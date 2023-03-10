from typing import Type

from data.hub.hub_ids.multi_task_hub_id import MultiStageHubId
from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.csv_project_reader import CsvProjectReader


class GitHubId(MultiStageHubId):
    """
    Identifies the dataset containing slice of git links from Jinfeng's crawl.
    """

    def __init__(self, **kwargs):
        """
        Initializes multi stage with task set to none.
        """
        if "task" in kwargs:
            raise Exception("Task cannot be defined for single-task dataset.")
        super().__init__(task=None, **kwargs)

    def get_project_path(self, data_dir: str) -> str:
        project_path = super().get_project_path(data_dir)
        return project_path + ".csv"

    def get_url(self) -> str:
        """
        :return: Returns URL to hub dataset.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/open-source/git.zip"

    @staticmethod
    def get_project_reader() -> Type[AbstractProjectReader]:
        return CsvProjectReader
