from gen_common.data.hub.abstract_hub_id import AbstractHubId


class MipHubId(AbstractHubId):
    """
    Describes the medical infusion pump dataset.
    """

    def get_url(self) -> str:
        """
        :return: Returns the URL to the medical infusion pump dataset in Hub.
        """
        return "https://safa-datasets-open.s3.amazonaws.com/datasets/open-source/mip.zip"
