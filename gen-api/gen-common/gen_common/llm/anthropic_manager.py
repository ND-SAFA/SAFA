import logging
from typing import Dict, List, Optional, Set, Tuple, TypedDict, Union

import anthropic

from gen_common.constants import anthropic_constants, environment_constants
from gen_common.constants.environment_constants import ANTHROPIC_KEY
from gen_common.constants.symbol_constants import EMPTY_STRING
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.infra.t_threading.threading_state import MultiThreadState
from gen_common.llm.abstract_llm_manager import AbstractLLMManager
from gen_common.llm.anthropic_exception_handler import anthropic_exception_handler
from gen_common.llm.args.anthropic_args import AnthropicArgs, AnthropicParams
from gen_common.llm.llm_responses import GenerationResponse, \
    SupportedLLMResponses
from gen_common.llm.llm_task import LLMCompletionType
from gen_common.llm.prompts.llm_prompt_build_args import LLMPromptBuildArgs
from gen_common.util.attr_dict import AttrDict
from gen_common.util.dict_util import DictUtil
from gen_common.util.thread_util import ThreadUtil


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


logging.getLogger("httpx").setLevel(logging.WARNING)


class AnthropicManager(AbstractLLMManager[AnthropicResponse]):
    """
    Defines AI interface for anthropic API.
    """

    NOT_IMPLEMENTED_ERROR = "Anthropic has not implemented fine-tuned models."
    prompt_args = LLMPromptBuildArgs(prompt_prefix=EMPTY_STRING, prompt_suffix=EMPTY_STRING, completion_prefix=" ",
                                     completion_suffix="###", build_system_prompts=True)

    def __init__(self, llm_args: AnthropicArgs = None):
        """
        Initializes with args used for the requests to Anthropic's model
        :param llm_args: args used for the requests to Anthropic's model
        """
        if llm_args is None:
            llm_args = AnthropicArgs()
        assert isinstance(llm_args, AnthropicArgs), "Must use Anthropic args with Anthropic manager"
        super().__init__(llm_args=llm_args, prompt_args=self.prompt_args)

    def make_completion_request_impl(self, raise_exception: bool = True, original_responses: List = None,
                                     retries: Set[int] = None, **params) -> MultiThreadState:
        """
        Makes a completion request to anthropic api.
        :param raise_exception: If True, raises an exception if the request has failed.
        :param original_responses: List of the original responses from the model if retrying.
        :param retries: Set of indices of responses that need retried because they failed the first time.
        :param params: Named parameters to anthropic API.
        :return: Anthropic's response to completion request.
        """
        assert AnthropicParams.PROMPT in params, f"Expected {params} to include `prompt`"
        prompts = params.pop(AnthropicParams.PROMPT)
        if isinstance(prompts, str):
            prompts = self.format_prompts(prompts)
        system_prompts = DictUtil.get_dict_values(params, pop=True, system=[None] * len(prompts))
        if not isinstance(system_prompts, list):
            system_prompts = [system_prompts]
        if AnthropicParams.MODEL not in params:
            params[AnthropicParams.MODEL] = self.llm_args.model
        else:
            assert params[
                       AnthropicParams.MODEL] == self.llm_args.model, f"Expected model to be {self.llm_args.model} but got {params[AnthropicParams.MODEL]}"
        logger.info(f"Starting Anthropic batch ({len(prompts)}): {params['model']}")

        anthropic_client = get_client()

        def thread_work(payload: Tuple[int, str]) -> Dict:
            """
            Performs completion on prompt and sets response to index.
            :param payload: Payload containing the index to set response to and the prompt to complete.
            :return: None
            """
            index, prompt = payload
            system_prompt = system_prompts[index]
            prompt_params = {**params, AnthropicParams.MESSAGES: prompt}
            if system_prompt is not None:
                prompt_params[AnthropicParams.SYSTEM] = system_prompt
            local_response = anthropic_client.messages.create(**prompt_params)
            return local_response

        global_state: MultiThreadState = ThreadUtil.multi_thread_process("Completing prompts", list(enumerate(prompts)),
                                                                         thread_work,
                                                                         retries=retries,
                                                                         collect_results=True,
                                                                         n_threads=anthropic_constants.ANTHROPIC_MAX_THREADS,
                                                                         max_attempts=anthropic_constants.ANTHROPIC_MAX_RE_ATTEMPTS,
                                                                         raise_exception=raise_exception,
                                                                         rpm=anthropic_constants.ANTHROPIC_MAX_RPM,
                                                                         exception_handlers=[anthropic_exception_handler])
        close_client(anthropic_client)
        if raise_exception and global_state.exception:
            raise global_state.exception

        self._handle_exceptions(global_state)
        global_responses = global_state.results
        for i, res in enumerate(global_responses):
            if isinstance(res, Exception):
                if raise_exception:
                    raise res
                global_state.failed_responses.add(i)
        if retries is not None:
            global_responses = self._combine_original_responses_and_retries(global_responses, original_responses, retries)
        global_state.results = [res for res in global_responses]
        return global_state

    def translate_to_response(self, task: LLMCompletionType, res: List[AnthropicResponse],
                              **params) -> Optional[SupportedLLMResponses]:
        """
        Translates the LLM library response to task specific response.
        :param task: The task to translate to.
        :param res: The response from the LLM library.
        :param params: Any additional parameters to customize translation.
        :return: A task-specific response.
        """
        texts = [self._extract_response(r) for r in res]
        return GenerationResponse(texts)

    @classmethod
    def format_response(cls, response_text: str = None, exception: Exception = None) -> AttrDict:
        """
        Formats the text, exception and any other information in the same way as all other responses from OpenAI.
        :param response_text: The models generated text.
        :param exception: Any exception raised during the generation.
        :return: The formatted response
        """
        response = AttrDict()
        if response_text:
            response["content"] = [AttrDict({"text": response_text})]
        if exception:
            response["error"] = exception
        return response

    @staticmethod
    def _extract_response(res: dict) -> Union[str, Exception]:
        """
        Gets the LLM response or the error msg if exception occurred.
        :param res: The response.
        :return: The LLM response or the error msg if exception occurred
        """
        if hasattr(res, "content"):
            return res.content[0].text
        else:
            return Exception(res["error"])


def get_client():
    """
    Returns the current anthropic client.
    :return:  Returns the singleton anthropic client.
    """
    if environment_constants.IS_TEST:
        from gen_common.infra.mock.anthropic import MockAnthropicClient
        return MockAnthropicClient()
    else:
        assert ANTHROPIC_KEY, f"Must supply value for {ANTHROPIC_KEY} "
        return anthropic.Client(api_key=ANTHROPIC_KEY)


def close_client(anthropic_client: anthropic.Client) -> None:
    """
    If anthropic client is given, then protected session is closed.
    :param anthropic_client: Mock client or anthropic client.
    :return: None
    """
    if hasattr(anthropic_client, "_session"):
        anthropic_client._session.close()
        logger.info("Anthropic connection has been closed.")
