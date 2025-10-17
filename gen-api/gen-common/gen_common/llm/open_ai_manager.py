from collections import namedtuple
from typing import List, Set
from unittest.mock import MagicMock

import openai

from gen_common.constants import environment_constants, open_ai_constants
from gen_common.constants.environment_constants import OPEN_AI_KEY
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.infra.t_threading.threading_state import MultiThreadState
from gen_common.llm.abstract_llm_manager import AIObject, AbstractLLMManager
from gen_common.llm.args.open_ai_args import OpenAIArgs, OpenAIParams
from gen_common.llm.llm_responses import GenerationResponse, \
    SupportedLLMResponses
from gen_common.llm.llm_task import LLMCompletionType
from gen_common.llm.prompts.llm_prompt_build_args import LLMPromptBuildArgs
from gen_common.util.attr_dict import AttrDict
from gen_common.util.thread_util import ThreadUtil

Res = namedtuple('Res', ['choices'])


class OpenAIManager(AbstractLLMManager[AttrDict]):
    prompt_args = LLMPromptBuildArgs(prompt_prefix="", prompt_suffix="\n>", completion_prefix="", completion_suffix="",
                                     build_system_prompts=False)

    def __init__(self, llm_args: OpenAIArgs = None):
        """
        Initializes with args used for the requests to Anthropic model
        :param llm_args: args used for the requests to Anthropic model
        """
        if llm_args is None:
            llm_args = OpenAIArgs(prompt_args=self.prompt_args)
        assert isinstance(llm_args, OpenAIArgs), "Must use OpenAI args with OpenAI manager"
        llm_args.prompt_args = self.prompt_args
        super().__init__(llm_args=llm_args, prompt_args=self.prompt_args)
        logger.info(f"Created OpenAI manager with Model: {self.llm_args.model}")

    def make_completion_request_impl(self, raise_exception: bool = True, original_responses: List = None,
                                     retries: Set[int] = None, **params) -> AIObject:
        """
        Makes a request to completion a model
        :param raise_exception: If True, raises an exception if the request has failed.
        :param original_responses: List of the original responses from the model if retrying.
        :param retries: Set of indices of responses that need retried because they failed the first time.
        :param params: Params necessary for request
        :return: The response from open  ai
        """
        params.pop(OpenAIParams.LOG_PROBS)
        prompts = params.pop(OpenAIParams.PROMPT)
        logger.info(f"Starting OpenAI batch: {params['model']}")

        def complete_prompt(p: str) -> str:
            """
            Completes the prompt with openai manager.
            :param p: The prompt to complete.
            :return: The response as a string.
            """
            params[OpenAIParams.MESSAGES] = p
            res = self._make_request(**params)
            return res.choices[0]

        global_state: MultiThreadState = ThreadUtil.multi_thread_process("Making completion requests",
                                                                         prompts,
                                                                         complete_prompt,
                                                                         raise_exception=raise_exception,
                                                                         n_threads=open_ai_constants.OPENAI_MAX_THREADS,
                                                                         max_attempts=open_ai_constants.OPENAI_MAX_ATTEMPTS,
                                                                         retries=retries,
                                                                         collect_results=True)

        self._handle_exceptions(global_state)

        global_responses = global_state.results
        if retries:
            global_responses = self._combine_original_responses_and_retries(global_responses, original_responses, retries)
        global_state.results = Res(choices=global_responses)
        return global_state

    @staticmethod
    def translate_to_response(task: LLMCompletionType, res: AttrDict, **params) -> SupportedLLMResponses:
        """
        Translates the response to the response for task.
        :param task: The task to translate to.
        :param res: OpenAI response.
        :param params: The parameters to the API.
        :return: A response for the supported types.
        """
        text_responses = [choice.message["content"].strip() if choice.message else choice.exception
                          for choice in res.choices]
        return GenerationResponse(text_responses)

    def upload_file(self, **params) -> AttrDict:
        """
        Makes a request to upload a file
        :param params: Params necessary for request
        :return: The response from open  ai
        """
        return openai.File.create(**params)

    @classmethod
    def format_response(cls, response_text: str = None, exception: Exception = None) -> AttrDict:
        """
        Formats the text, exception and any other information in the same way as all other responses from OpenAI.
        :param response_text: The models generated text.
        :param exception: Any exception raised during the generation.
        :return: The formatted response
        """
        response = AttrDict({"message": None, "log_probs": None})
        if response_text:
            response.message = {"content": response_text}
        if exception:
            response["exception"] = exception
        return response

    @staticmethod
    def _make_request(**params) -> AttrDict:
        """
        Makes a request to open ai.
        :param params: Parameters for the request.
        :return: The response from open ai.
        """
        if not environment_constants.IS_TEST:
            assert OPEN_AI_KEY, f"Must supply value for {f'{OPEN_AI_KEY=}'.split('=')[0]} in .env"
            openai.api_key = OPEN_AI_KEY
        else:
            assert isinstance(openai.ChatCompletion.create, MagicMock), "Should not make real request if in test mode!!"
        res = openai.ChatCompletion.create(**params)
        return res
