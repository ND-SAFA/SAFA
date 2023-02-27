from data.hub.abstract_hub_id import AbstractHubId
from data.hub.hub_ids.multi_task_hub_id import MultiTaskHubId
from util.override import overrides


class DroneHubId(MultiTaskHubId):
    """
    Describes the DroneResponse project reader.
    """

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to DroneResponse on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/open-source/drone.zip"
