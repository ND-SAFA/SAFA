from typing import TypedDict

import anthropic
from tqdm import tqdm

from tgen.constants.anthropic_constants import ANTHROPIC_KEY
from tgen.constants.environment_constants import IS_TEST
from tgen.util.llm.llm_util import LLMUtil


class AnthropicResponse(TypedDict):
    """
    Contains anthropic response to their API.
    """


class AnthropicUtil(LLMUtil[AnthropicResponse]):
    """
    Defines AI interface for anthropic API.
    """
    Client = None
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
        assert "prompt" in params, f"Expected {params} to include `params`"
        prompts = params["prompt"]
        response = []
        if isinstance(prompts, list):
            for prompt in tqdm(params["prompt"]):
                prompt_params = {**params, "prompt": prompt}
                prompt_response = AnthropicUtil.Client.completion(**prompt_params)
                response.append(prompt_response)
        elif isinstance(prompts, str):
            prompt_response = AnthropicUtil.Client.completion(**params)
            response.append(prompt_response)
        else:
            raise Exception(f"Prompt format is not supported. Expected list or string: {prompts}")
        return response

    @staticmethod
    def upload_file(**params) -> AnthropicResponse:
        """
        Raises exception noting that anthropic has not implemented this feature.
        :param params: Ignored.
        :return: None
        """
        raise NotImplementedError(NotImplementedError)


if not IS_TEST:
    assert ANTHROPIC_KEY, f"Must supply value for {ANTHROPIC_KEY} "
    if AnthropicUtil.Client is None:
        AnthropicUtil.Client = anthropic.Client(ANTHROPIC_KEY)
