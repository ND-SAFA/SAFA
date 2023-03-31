import os

from cloud.gcp_cloud_storage import GcpCloudStorage
from cloud.icloud_storage import ICloudStorage
from util.supported_enum import SupportedEnum


class SupportedCloudStorage(SupportedEnum):
    """
    Enumerates supported storage solutions.
    """
    GCP = GcpCloudStorage

    @classmethod
    def get_storage(cls) -> ICloudStorage:
        """
        :return: Returns the cloud storage defined in environment.
        """
        return cls.get_value(os.environ["STORAGE"])
