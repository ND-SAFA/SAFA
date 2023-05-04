from typing import List, TypedDict

import anthropic
from tqdm import tqdm

from tgen.constants.environment_constants import ANTHROPIC_KEY, IS_TEST
from tgen.train.args.anthropic_args import AnthropicParams
from tgen.util.llm.llm_responses import GenerationResponse, SupportedLLMResponses
from tgen.util.llm.llm_task import LLMTask
from tgen.util.llm.llm_util import LLMUtil


class AnthropicResponse(TypedDict):
    """
    Contains anthropic response to their API.
    """
    completion: str
    stop: str
    stop_reason: str
    truncated: bool
    log_id: str
    model: str
    exception: str


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
    def make_completion_request_impl(**params) -> AnthropicResponse:
        """
        Makes a completion request to anthropic api.
        :param params: Named parameters to anthropic API.
        :return: Anthropic's response to completion request.
        """
        assert AnthropicParams.PROMPT in params, f"Expected {params} to include `params`"
        prompts = params["prompt"]
        response = []
        if isinstance(prompts, str):
            prompts = [prompts]
        for p in tqdm(prompts):
            prompt_params = {**params, "prompt": p}
            prompt_response = AnthropicUtil.Client.completion(**prompt_params)
            response.append(prompt_response)
        return response

    @staticmethod
    def translate_to_response(task: LLMTask, res: List[AnthropicResponse], **params) -> SupportedLLMResponses:
        if task == LLMTask.GENERATION:
            return GenerationResponse([r["completion"] for r in res])
        raise NotImplementedError("Reading anthropic responses is under construction. Please use OpenAI for now.")

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
