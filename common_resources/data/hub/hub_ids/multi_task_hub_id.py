import os
from abc import ABC
from typing import List

from common_resources.tools.constants.model_constants import STAGES
from common_resources.data.hub.abstract_hub_id import AbstractHubId


class MultiStageHubId(AbstractHubId, ABC):
    """
    Provides base implementation for managing different tasks with different splits all from the same source file.
    """

    def __init__(self, task: str = "base", stage: str = None, local_path: str = None):
        """
        Initialized hub for given task at given stage.
        :param task: The type of task defined by this dataset.
        :param stage: The stage of the splits (e.g. train, val, eval).
        :param local_path: Optional path to local version of dataset.
        """
        super().__init__(local_path)
        self.task = task
        self.stage = stage

    def get_project_path(self, data_dir: str) -> str:
        """
        Returns path to stage definition file.
        :param data_dir: The base project path containing all stages.
        :return: Path to stage definition file.
        """
        project_path = data_dir
        tasks_defined = os.listdir(data_dir)
        project_path = self.add_if_exists(self.task, tasks_defined, project_path)
        project_path = self.add_if_exists(self.stage, STAGES, project_path)
        return project_path

    @staticmethod
    def add_if_exists(module: str, defined_modules: List[str], base_path: str):
        """
        Adds module to base path if defined.
        :param module: The module to be added to path.
        :param defined_modules: List of defined modules to check existence in.
        :param base_path: The base path to append to.
        :return: The final path.
        """
        if module:
            assert module in defined_modules, f"Expected ({module}) to be one of ({defined_modules})."
            return os.path.join(base_path, module)
        return base_path
