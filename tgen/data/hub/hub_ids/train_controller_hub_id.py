from tgen.common.util.override import overrides
from tgen.data.hub.abstract_hub_id import AbstractHubId


class TrainControllerHubId(AbstractHubId):
    """
    Describes the TrainController project reader.
    """

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to TrainController on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/open-source/traincontroller.zip"
