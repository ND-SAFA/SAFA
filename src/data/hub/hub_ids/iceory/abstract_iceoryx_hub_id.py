from abc import ABC, abstractmethod

from data.hub.abstract_hub_id import AbstractHubId
from util.override import overrides


class IceoryxHubId(AbstractHubId, ABC):
    """
    Identifier iceoryx open source project.
    """

    @staticmethod
    @abstractmethod
    def get_zip_name() -> str:
        """
        :return: Returns the name of the zip file.
        """

    @classmethod
    @overrides(AbstractHubId)
    def get_url(cls) -> str:
        """
        :return: Returns URL to CCHIT on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/iceoryx/code.zip"
