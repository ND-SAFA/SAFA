from typing import Dict, List, Optional, TypedDict

import anthropic

from tgen.constants.anthropic_constants import ANTHROPIC_MAX_THREADS
from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.constants.environment_constants import ANTHROPIC_KEY, IS_TEST
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import ClassificationResponse, GenerationResponse, SupportedLLMResponses
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.args.anthropic_args import AnthropicArgs, AnthropicParams
from tgen.util.logging.logger_manager import logger
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


def response_with_defaults(**params) -> AnthropicResponse:
    """
    Creates an Anthropic response using default values unless provided
    :param params: Params to use in place of defaults
    :return: The Anthropic response with defaults filled in
    """
    defaults = {str: EMPTY_STRING, bool: False}
    all_params = {attr: params[attr] if attr in params else defaults[type_]
                  for attr, type_ in AnthropicResponse.__annotations__.items()}
    return AnthropicResponse(**all_params)


class AnthropicManager(AbstractLLMManager[AnthropicResponse]):
    """
    Defines AI interface for anthropic API.
    """

    Client = None
    NOT_IMPLEMENTED_ERROR = "Anthropic has not implemented fine-tuned models."
    prompt_args = PromptArgs(prompt_prefix="\n\nHuman: ", prompt_suffix="\n\nAssistant:", completion_prefix=" ",
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
        logger.info(f"Created Anthropic manager with Model: {self.llm_args.model}")

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
        assert AnthropicParams.PROMPT in params, f"Expected {params} to include `prompt`"
        logger.info(f"Starting Anthropic batch: {params['model']}")
        prompts = params[AnthropicParams.PROMPT]
        response = []
        if isinstance(prompts, str):
            prompts = [prompts]

        response = [None] * len(prompts)

        def thread_work(payload):
            index, prompt = payload
            prompt_params = {**params, AnthropicParams.PROMPT: prompt}
            # prompt_params = {'model': 'claude-instant-v1-100k', 'temperature': 0.0, 'max_tokens_to_sample': 1,
            #                  'prompt': "\n\nHuman: Below are software artifacts from the same project. Ignoring the abstraction levels of the artifacts, are (1) and (2) part of the same feature? Answer 'yes' or 'no'.\n\n1. UAV type specification assignment The VehicleCore shall associate a {{{{UAV_TYPE}}}} for each UAV defining its basic attributes\n\n2. UAV type specification assignment Each Virtual and Physical drone is associated with a predefined {{{{UAV_TYPE}}}} defining its basic attributes.\n\nAssistant:"}
            try:
                prompt_response = AnthropicManager.Client.completion(**prompt_params)
            except Exception as e:
                prompt_response = response_with_defaults(exception=str(e))
            response[index] = prompt_response

        ThreadUtil.multi_thread_process("Completing prompts", list(enumerate(prompts)), thread_work, ANTHROPIC_MAX_THREADS)

        for res in response:
            if res and res.get("exception", EMPTY_STRING):
                raise Exception(res["exception"])
        return [res for res in response if res is not None]

    def translate_to_response(self, task: LLMCompletionType, res: List[AnthropicResponse], **params) -> Optional[
        SupportedLLMResponses]:
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
            results = [AnthropicManager._get_log_prob(r["completion"]) for r in res]
            return ClassificationResponse(results)
        else:
            raise ValueError(f"Response is not supported by anthropic manager: {task}")

    @staticmethod
    def upload_file(**params) -> AnthropicResponse:
        """
        Raises exception noting that anthropic has not implemented this feature.
        :param params: Ignored.
        :return: None
        """
        raise NotImplementedError(NotImplementedError)

    @staticmethod
    def _get_log_prob(completion: str) -> Dict[str, float]:
        """
        Gets the log probabilities for a classification completion
        :param completion: The completion
        :return: The log probabilities for each class
        """
        completion = completion.lower()
        log_probs = {"yes": 0, "no": 0}  # TODO get the neg and pos clas from the prompt creator
        response_2_index = {ans: completion.find(ans) for ans in log_probs.keys()}
        response_2_index = {k: v for k, v in response_2_index.items() if v != -1}  # remove if response not in completion
        first_response = min(response_2_index, key=response_2_index.get) if len(response_2_index) > 0 else None
        if first_response in log_probs:
            log_probs[first_response] = 1
        else:
            log_probs = {k: 0.5 for k in log_probs.keys()}
        return log_probs


if not IS_TEST:
    assert ANTHROPIC_KEY, f"Must supply value for {ANTHROPIC_KEY} "
    if AnthropicManager.Client is None:
        AnthropicManager.Client = anthropic.Client(ANTHROPIC_KEY)
