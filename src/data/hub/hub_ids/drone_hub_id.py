import os

from constants import STAGES
from data.hub.abstract_hub_id import AbstractHubId
from data.hub.hub_ids.multi_task_hub_id import MultiTaskHubId
from data.keys.safa_format import SafaKeys
from util.override import overrides


class DroneHubId(MultiTaskHubId):
    """
    Describes the DroneResponse project reader.
    """

    def __init__(self, task: str, stage: str = None):
        """
        Loads stage of Drone programming language task.
        :param stage: Either train, val, or eval
        """
        super().__init__(task, stage)

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to DroneResponse on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/drone.zip"

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
