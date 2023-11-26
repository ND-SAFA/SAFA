import os

from api.cloud.gcp_cloud_storage import GcpCloudStorage
from api.cloud.icloud_storage import ICloudStorage
from tgen.util.supported_enum import SupportedEnum


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
        storage_provider = os.environ.get("STORAGE", "GCP")
        return cls.get_value(storage_provider)
