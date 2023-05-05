from typing import List, TypedDict

import anthropic
from tqdm import tqdm

from tgen.constants.environment_constants import ANTHROPIC_KEY, IS_TEST
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import GenerationResponse, SupportedLLMResponses
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.args.anthropic_args import AnthropicArgs, AnthropicParams


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


class AnthropicManager(AbstractLLMManager[AnthropicResponse]):
    """
    Defines AI interface for anthropic API.
    """

    Client = None
    NOT_IMPLEMENTED_ERROR = "Anthropic has not implemented fine-tuned models."

    def __init__(self, llm_args: AnthropicArgs):
        """
        Initializes with args used for the requests to Anthropic's model
        :param llm_args: args used for the requests to Anthropic's model
        """
        assert isinstance(llm_args, AnthropicArgs), "Must use Anthropic args with Anthropic manager"
        prompt_args = PromptArgs(prompt_prefix="\n\nHuman:", prompt_suffix="\n\nAssistant:", completion_prefix=" ",
                                 completion_suffix="###")
        super().__init__(llm_args=llm_args, prompt_args=prompt_args)

    def _make_fine_tune_request_impl(self, **kwargs) -> AnthropicResponse:
        """
        Raises exception noting that anthropic has not implemented this feature.
        :param kwargs: Ignored.
        :return: None
        """
        raise NotImplementedError(NotImplementedError)

    def retrieve_fine_tune_request(self, completion_type: LLMCompletionType, **kwargs) -> AnthropicResponse:
        """
        Raises exception noting that anthropic has not implemented this feature.
        :param kwargs: Ignored.
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
            prompt_response = AnthropicManager.Client.completion(**prompt_params)
            response.append(prompt_response)
        return response

    @staticmethod
    def translate_to_response(task: LLMCompletionType, res: List[AnthropicResponse], **params) -> SupportedLLMResponses:
        if task == LLMCompletionType.GENERATION:
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
    if AnthropicManager.Client is None:
        AnthropicManager.Client = anthropic.Client(ANTHROPIC_KEY)
