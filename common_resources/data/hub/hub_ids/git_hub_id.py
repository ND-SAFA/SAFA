from typing import Type

from common_resources.tools.util.dict_util import DictUtil
from common_resources.data.hub.hub_ids.multi_task_hub_id import MultiStageHubId
from common_resources.data.readers.abstract_project_reader import AbstractProjectReader
from common_resources.data.readers.csv_project_reader import CsvProjectReader


class GitHubId(MultiStageHubId):
    """
    Identifies the dataset containing slice of git links from Jinfeng's crawl.
    """

    def __init__(self, **kwargs):
        """
        Initializes multi stage with task set to none.
        """
        if DictUtil.get_dict_values(kwargs, task=None) is not None:
            raise Exception("Task cannot be defined for single-task dataset.")
        super().__init__(task=None, **kwargs)

    def get_project_path(self, data_dir: str) -> str:
        """
        Returns the path to CSV file containing git links.
        :param data_dir: Path to directory containing project data.
        :return: Project path.
        """
        project_path = super().get_project_path(data_dir)
        return project_path + ".csv"

    def get_url(self) -> str:
        """
        :return: Returns URL to hub dataset.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/open-source/git.zip"

    @staticmethod
    def get_project_reader() -> Type[AbstractProjectReader]:
        """
        :return: Returns project reader for csv file containing git links.
        """
        return CsvProjectReader
