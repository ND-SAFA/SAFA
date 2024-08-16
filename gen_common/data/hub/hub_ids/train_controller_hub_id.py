from gen_common.data.hub.abstract_hub_id import AbstractHubId
from gen_common.util.override import overrides


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
