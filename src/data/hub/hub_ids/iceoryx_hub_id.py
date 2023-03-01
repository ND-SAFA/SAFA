from abc import ABC

from data.hub.abstract_hub_id import AbstractHubId
from data.hub.hub_ids.multi_task_hub_id import MultiStageHubId
from util.override import overrides


class IceoryxHubId(MultiStageHubId, ABC):
    """
    Identifier iceoryx open source project.
    """

    @classmethod
    @overrides(AbstractHubId)
    def get_url(cls) -> str:
        """
        :return: Returns Bucket URL to dataset.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/iceoryx.zip"
