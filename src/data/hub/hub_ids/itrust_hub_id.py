import os.path

from data.hub.abstract_hub_id import AbstractHubId
from data.hub.hub_ids.multi_task_hub_id import MultiTaskHubId
from util.override import overrides


class ITrustHubId(MultiTaskHubId):
    """
    Describes the iTrust project reader.
    """

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to iTrust on the SAFA bucket containing definition file.
        """
        if self.local_path:
            return os.path.expanduser(self.local_path)
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/open-source/itrust.zip"
