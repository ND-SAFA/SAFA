from tgen.util.ai.ai_util import AIObject, AiUtil


class AnthropicUtil(AiUtil):
    """
    Defines AI interface for anthropic API.
    """

    @staticmethod
    def make_fine_tune_request(**params) -> AIObject:
        raise NotImplementedError()

    @staticmethod
    def retrieve_fine_tune_request(**params) -> AIObject:
        raise NotImplementedError()

    @staticmethod
    def make_completion_request(**params) -> AIObject:
        raise NotImplementedError()

    @staticmethod
    def upload_file(**params) -> AIObject:
        raise NotImplementedError()
