from collections import namedtuple
from typing import List, Set
from unittest.mock import MagicMock

import openai
from openai.openai_object import OpenAIObject

from tgen.common.constants import open_ai_constants
from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.environment_constants import IS_TEST, OPEN_AI_KEY, OPEN_AI_ORG
from tgen.common.logging.logger_manager import logger
from tgen.common.threading.threading_state import MultiThreadState
from tgen.common.util.attr_dict import AttrDict
from tgen.common.util.thread_util import ThreadUtil
from tgen.core.args.open_ai_args import OpenAIArgs, OpenAIParams
from tgen.models.llm.abstract_llm_manager import AIObject, AbstractLLMManager
from tgen.models.llm.llm_responses import ClassificationItemResponse, ClassificationResponse, GenerationResponse, SupportedLLMResponses
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.llm_prompt_build_args import LLMPromptBuildArgs

Res = namedtuple('Res', ['choices'])


class OpenAIManager(AbstractLLMManager[OpenAIObject]):
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

    def _make_fine_tune_request_impl(self, **kwargs) -> OpenAIObject:
        """
        Makes a request to fine-tune a model
        :param kwargs: Params necessary for request
        :return: The response from open  ai
        """
        result = openai.FineTune.create(**kwargs)
        if result is None:  # retry if failed.
            result = openai.FineTune.create(**kwargs)
        return result

    def retrieve_fine_tune_request(self, **params) -> OpenAIObject:
        """
        Retrieves s a request to fine-tune a model
        :return: The response from open  ai
        """
        return openai.FineTune.retrieve(**params)

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
        prompt = params.pop(OpenAIParams.PROMPT)
        prompts = prompt if isinstance(prompt, list) else [prompt]
        logger.info(f"Starting OpenAI batch: {params['model']}")

        def complete_prompt(p: str) -> str:
            """
            Completes the prompt with openai manager.
            :param p: The prompt to complete.
            :return: The response as a string.
            """
            params[OpenAIParams.MESSAGES] = [self.convert_prompt_to_message(p)]
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
    def extract_all_text_from_response(res: OpenAIObject) -> str:
        """
        Extracts all text across all batches from the response
        :param res: The response
        :return: All text across all batches from the response
        """
        return EMPTY_STRING.join([res.message["content"] for res in res.choices if res.message])

    @staticmethod
    def translate_to_response(task: LLMCompletionType, res: OpenAIObject, **params) -> SupportedLLMResponses:
        """
        Translates the response to the response for task.
        :param task: The task to translate to.
        :param res: OpenAI response.
        :param params: The parameters to the API.
        :return: A response for the supported types.
        """
        text_responses = [choice.message["content"].strip() if choice.message else choice.exception
                          for choice in res.choices]
        if task == LLMCompletionType.GENERATION:
            return GenerationResponse(text_responses)
        elif task == LLMCompletionType.CLASSIFICATION:
            probs = [r.logprobs.top_logprobs[0] if r.logprobs else None for r in res.choices]
            classification_items = [ClassificationItemResponse(t, probs=p) for t, p in zip(text_responses, probs)]
            return ClassificationResponse(classification_items)
        else:
            raise NotImplementedError(f"No handler for {task.name} is implemented")

    def upload_file(self, **params) -> OpenAIObject:
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
        if not IS_TEST:
            assert OPEN_AI_ORG and OPEN_AI_KEY, f"Must supply value for {f'{OPEN_AI_ORG=}'.split('=')[0]} " \
                                                f"and {f'{OPEN_AI_KEY=}'.split('=')[0]} in .env"
            openai.organization = OPEN_AI_ORG
            openai.api_key = OPEN_AI_KEY
        else:
            assert isinstance(openai.ChatCompletion.create, MagicMock), "Should not make real request if in test mode!!"
        res = openai.ChatCompletion.create(**params)
        return res
