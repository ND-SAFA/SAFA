from gen_common.data.hub.abstract_hub_id import AbstractHubId
from gen_common.data.hub.hub_ids.multi_task_hub_id import MultiStageHubId
from gen_common.util.override import overrides


class JplHubId(MultiStageHubId):
    """
    Describes the DroneResponse project reader.
    """

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to DroneResponse on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/open-source/jpl.zip"
