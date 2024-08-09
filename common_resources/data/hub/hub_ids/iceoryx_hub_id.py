from abc import ABC

from common_resources.tools.util.override import overrides
from common_resources.data.hub.abstract_hub_id import AbstractHubId
from common_resources.data.hub.hub_ids.multi_task_hub_id import MultiStageHubId


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
