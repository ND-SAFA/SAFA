from data.hub.hub_ids.iceory.code.iceoryx_code import IceoryxCode


class IceoryxCodeEval(IceoryxCode):
    """
    Identifier iceoryx open source project.
    """

    @staticmethod
    def get_stage_name() -> str:
        """
        :return: Returns the name of the eval data file.
        """
        return "code_eval"
