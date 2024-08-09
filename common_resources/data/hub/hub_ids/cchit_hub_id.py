from common_resources.tools.util.override import overrides
from common_resources.data.hub.abstract_hub_id import AbstractHubId


class CCHITHubId(AbstractHubId):
    """
    Describes the CCHIT project reader.
    """

    @overrides(AbstractHubId)
    def get_url(self) -> str:
        """
        :return: Returns URL to CCHIT on the SAFA bucket containing definition file.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/open-source/cchit.zip"
