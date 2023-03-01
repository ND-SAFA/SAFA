import os
from abc import ABC

from constants import STAGES
from data.hub.abstract_hub_id import AbstractHubId
from data.keys.safa_format import SafaKeys


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

    def get_definition_path(self, data_dir: str) -> str:
        """
        Returns path to stage definition file.
        :param data_dir: The base project path containing all stages.
        :return: Path to stage definition file.
        """
        if self.stage:
            tasks_defined = os.listdir(data_dir)
            assert self.task in tasks_defined, f"Task () is not one of: {tasks_defined}"
            assert self.stage in STAGES, f"Stage () is not one of: {STAGES}"
            return os.path.join(data_dir, self.task, self.stage, SafaKeys.TIM_FILE)
        return os.path.join(data_dir, self.task, SafaKeys.TIM_FILE)
