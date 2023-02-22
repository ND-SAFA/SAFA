from data.hub.hub_ids.iceory.abstract_iceoryx_hub_id import IceoryxHubId


class IceoryxTrain(IceoryxHubId):
    """
    Identifier iceoryx open source project.
    """

    @staticmethod
    def get_stage_name() -> str:
        """
        :return: Returns the name of the training data file.
        """
        return "train"
