import math
from typing import List, TypedDict

import anthropic

from tgen.constants.anthropic_constants import ANTHROPIC_MAX_THREADS
from tgen.constants.environment_constants import ANTHROPIC_KEY, IS_TEST
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import ClassificationResponse, GenerationResponse, SupportedLLMResponses
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.args.anthropic_args import AnthropicArgs, AnthropicParams
from tgen.util.thread_util import ThreadUtil


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
    prompt_args = PromptArgs(prompt_prefix="\n\nHuman:", prompt_suffix="\n\nAssistant:", completion_prefix=" ",
                             completion_suffix="###")

    def __init__(self, llm_args: AnthropicArgs = None):
        """
        Initializes with args used for the requests to Anthropic's model
        :param llm_args: args used for the requests to Anthropic's model
        """
        if llm_args is None:
            llm_args = AnthropicArgs()
        assert isinstance(llm_args, AnthropicArgs), "Must use Anthropic args with Anthropic manager"
        super().__init__(llm_args=llm_args, prompt_args=self.prompt_args)

    def _make_fine_tune_request_impl(self, **kwargs) -> AnthropicResponse:
        """
        Raises exception noting that anthropic has not implemented this feature.
        :param kwargs: Ignored.
        :return: None
        """
        raise NotImplementedError(NotImplementedError)

    def retrieve_fine_tune_request(self, **kwargs) -> AnthropicResponse:
        """
        Raises exception noting that anthropic has not implemented this feature.
        :param kwargs: Ignored.
        :return: None
        """
        raise NotImplementedError(NotImplementedError)

    @staticmethod
    def make_completion_request_impl(**params) -> List[AnthropicResponse]:
        """
        Makes a completion request to anthropic api.
        :param params: Named parameters to anthropic API.
        :return: Anthropic's response to completion request.
        """
        assert AnthropicParams.PROMPT in params, f"Expected {params} to include `params`"
        prompts = params[AnthropicParams.PROMPT]
        response = []
        if isinstance(prompts, str):
            prompts = [prompts]

        response = [None] * len(prompts)

        def thread_work(payload):
            index, prompt = payload
            prompt_params = {**params, AnthropicParams.PROMPT: prompt}
            prompt_response = AnthropicManager.Client.completion(**prompt_params)
            response[index] = prompt_response

        ThreadUtil.multi_thread_process("Completing prompts", list(enumerate(prompts)), thread_work, ANTHROPIC_MAX_THREADS)

        return response

    def translate_to_response(self, task: LLMCompletionType, res: List[AnthropicResponse], **params) -> SupportedLLMResponses:
        """
        Translates the LLM library response to task specific response.
        :param task: The task to translate to.
        :param res: The response from the LLM library.
        :param params: Any additional parameters to customize translation.
        :return: A task-specific response.
        """
        if task == LLMCompletionType.GENERATION:
            return GenerationResponse([r["completion"] for r in res])
        if task == LLMCompletionType.CLASSIFICATION:
            results = []
            for r in res:
                r_completion = r["completion"].lower()
                yes_index = r_completion.find("yes")
                no_index = r_completion.find("no")
                log_probs = {}
                if yes_index == -1:
                    log_probs["yes"] = 0
                    yes_index = math.inf
                if no_index == -1:
                    log_probs["no"] = 0
                    no_index = math.inf
                if yes_index < no_index:
                    log_probs = {"yes": 1, "no": 0}
                else:
                    log_probs = {"yes": 0, "no": 1}
                if sum(log_probs.values()) == 0:
                    log_probs = {"yes": 0.5, "no": 0.5}

                results.append(log_probs)
            return ClassificationResponse(results)

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
