from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Set, Type, TypeVar, TypedDict, Union

from gen_common.constants.model_constants import PREDICT_TASK
from gen_common.infra.base_object import BaseObject
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.infra.t_threading.threading_state import MultiThreadState
from gen_common.llm.args.abstract_llm_args import AbstractLLMArgs
from gen_common.llm.llm_responses import SupportedLLMResponses
from gen_common.llm.llm_task import LLMCompletionType
from gen_common.llm.prompts.llm_prompt_build_args import LLMPromptBuildArgs

AIObject = TypeVar("AIObject")


class PromptRoles:
    USER = "user"
    ASSISTANT = "assistant"
    HUMAN = "human"
    AI = "ai"


ROLE_KEY = "role"
CONTENT_KEY = "content"


class Message(TypedDict):
    content: str
    role: str


class AbstractLLMManager(BaseObject, ABC, Generic[AIObject]):
    """
    Interface for all AI utility classes.
    """

    def __init__(self, llm_args: AbstractLLMArgs, prompt_args: LLMPromptBuildArgs):
        """
        Initializes the manager with args used for each request and the prompt args used for creating dataset
        :param llm_args: args used for each request
        :param prompt_args: args used for creating dataset
        """
        self.llm_args = llm_args
        self.prompt_args = prompt_args

    def make_completion_request(self, completion_type: LLMCompletionType,
                                prompt: Union[str, List],
                                original_responses: List = None,
                                raise_exception: bool = True,
                                **params) -> SupportedLLMResponses:
        """
        Makes a request to fine-tune a model.
        :param completion_type: The task to translate response to.
        :param prompt: The prompt(s) to use for completion.
        :param original_responses: List of the original responses from the model if retrying.
        :param raise_exception: If True, raises an exception if the request has failed.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """
        completion_params = self.llm_args.to_params(PREDICT_TASK, completion_type)
        completion_params.update(params)
        prompts = self.format_prompts(prompt)

        retries = self._get_indices_to_retry(original_responses, n_expected=len(prompts))

        global_state: MultiThreadState = self.make_completion_request_impl(raise_exception=raise_exception,
                                                                           original_responses=original_responses,
                                                                           retries=retries,
                                                                           prompt=prompts,
                                                                           **completion_params)
        llm_response = global_state.results
        translated_response = self.translate_to_response(completion_type, llm_response, **params)
        return translated_response

    def format_prompts(self, prompts: Union[List, str, Dict]) -> List[List[Message]]:
        """
        Formats the prompt for the anthropic api.
        :param prompts: Either a single prompt, a list of prompts, or a list of messages.
        :return: A list of conversations for the anthropic api.
        """
        if not isinstance(prompts, list) or isinstance(prompts[0], dict):
            prompts = [prompts]
        prompts_formatted = []
        for convo in prompts:
            if not isinstance(convo, list):
                if isinstance(convo, str):
                    convo = self.convert_prompt_to_message(convo)
                convo = [convo]
            prompts_formatted.append(convo)
        return prompts_formatted

    @staticmethod
    def convert_prompt_to_message(prompt: str, role: str = PromptRoles.USER) -> Message:
        """
        Converts a prompt to the expected format for messages between the user and assistant.
        :param prompt: The prompt/content of the message.
        :param role: The role specifies if the message is from the user or assistant.
        :return: Dictionary containing message content and role.
        """
        return Message(role=role, content=prompt)

    @abstractmethod
    def make_completion_request_impl(self, raise_exception: bool = True, original_responses: List = None,
                                     **params) -> AIObject:
        """
        Makes a completion request to model.
        :param raise_exception: If True, raises an exception if the request has failed.
        :param original_responses: List of the original responses from the model if retrying.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """

    @staticmethod
    @abstractmethod
    def translate_to_response(task: LLMCompletionType, res: AIObject, **params) -> SupportedLLMResponses:
        """
        Translates the LLM library response to task specific response.
        :param task: The task to translate to.
        :param res: The response from the LLM library.
        :param params: Any additional parameters to customize translation.
        :return: A task-specific response.
        """

    @classmethod
    @abstractmethod
    def format_response(cls, response_text: str = None, exception: Exception = None) -> SupportedLLMResponses:
        """
        Formats the text, exception and any other information in the same way as all other responses.
        :param response_text: The models generated text.
        :param exception: Any exception raised during the generation.
        :return: The formatted response
        """

    @classmethod
    def _handle_exceptions(cls, global_state: MultiThreadState) -> None:
        """
        Ensures that any exceptions are appropriately formatted.
        :param global_state: The global state from running the thread calls to the LLM.
        :param formatter: Handles formatting the exception in the format of the LLM (e.g. OpenAI vs. Anthropic)
        :return: None.
        """
        global_responses = global_state.results
        for i, res in enumerate(global_responses):
            if isinstance(res, Exception) or not res:
                e = global_state.exception if global_state.exception else Exception("Unknown Exception Occurred")
                global_responses[i] = cls.format_response(exception=e)
                global_state.failed_responses.add(i)

    @classmethod
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the supported enum class for LLM args.
        :param child_class_name: The name of the child to be created.
        :return: The supported enum class.
        """
        from gen_common.llm.supported_llm_manager import SupportedLLMManager
        return SupportedLLMManager

    @staticmethod
    def _get_indices_to_retry(original_responses: List[Any], n_expected: int) -> Set[int]:
        """
        Gets what indices need retried because of an exception from the original LLM responses.
        :param original_responses: The list of original responses.
        :param n_expected: The number of expected responses.
        :return: The set of indices that need retried because of an exception.
        """
        if original_responses is not None:
            if len(original_responses) == n_expected:
                retries = {i for i, r in enumerate(original_responses) if isinstance(r, Exception)}
                return retries
            else:
                logger.warning(f"Unable to reuse responses because the length does not match expected.")

    def _combine_original_responses_and_retries(self, new_response: List[Any], original_responses: List[Any],
                                                retries: Set[int]) -> List[SupportedLLMResponses]:
        """
        Combines the original responses with any that have been redone because they failed initially.
        :param new_response: The new response from the LLM.
        :param original_responses: The original responses.
        :param retries: List of indices of all responses that have been retried.
        :return: A list of all responses (both original and retried).
        """
        new_response = [(r if i in retries else self.format_response(response_text=original_responses[i]))
                        for i, r in enumerate(new_response)]
        return new_response
