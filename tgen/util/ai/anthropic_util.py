from typing import TypedDict

import anthropic

from tgen.constants import ANTHROPIC_KEY
from tgen.util.ai.ai_util import AiUtil


class AnthropicResponse(TypedDict):
    """
    Contains anthropic response to their API.
    """


class AnthropicUtil(AiUtil[AnthropicResponse]):
    """
    Defines AI interface for anthropic API.
    """
    CLIENT = None
    NOT_IMPLEMENTED_ERROR = "Anthropic has not implemented fine-tuned models."

    @staticmethod
    def make_fine_tune_request(**params) -> AnthropicResponse:
        """
        Raises exception noting that anthropic has not implemented this feature.
        :param params: Ignored.
        :return: None
        """
        raise NotImplementedError(NotImplementedError)

    @staticmethod
    def retrieve_fine_tune_request(**params) -> AnthropicResponse:
        """
        Raises exception noting that anthropic has not implemented this feature.
        :param params: Ignored.
        :return: None
        """
        raise NotImplementedError(NotImplementedError)

    @staticmethod
    def make_completion_request(**params) -> AnthropicResponse:
        """
        Makes a completion request to anthropic api.
        :param params: Named parameters to anthropic API.
        :return: Anthropic's response to completion request.
        """
        client = AnthropicUtil.get_client()
        return client.completion(**params)

    @staticmethod
    def upload_file(**params) -> AnthropicResponse:
        """
        Raises exception noting that anthropic has not implemented this feature.
        :param params: Ignored.
        :return: None
        """
        raise NotImplementedError(NotImplementedError)

    @staticmethod
    def get_client() -> anthropic.Client:
        """
        :return: Returns static client to anthropic model.
        """
        if AnthropicUtil.CLIENT is None:
            AnthropicUtil.CLIENT = anthropic.Client(ANTHROPIC_KEY)
        return AnthropicUtil.CLIENT
