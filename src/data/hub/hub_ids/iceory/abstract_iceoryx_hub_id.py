from abc import ABC

from data.hub.abstract_dataset_descriptor import AbstractHubId
from util.override import overrides


class IceoryxHubId(AbstractHubId, ABC):
    """
    Identifier iceoryx open source project.
    """

    @classmethod
    @overrides(AbstractHubId)
    def get_url(cls) -> str:
        """
        :return: Returns URL to CCHIT on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/iceoryx.zip"
