from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Set, Type, TypeVar, Union, TypedDict

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.logging.logger_manager import logger
from tgen.common.threading.threading_state import MultiThreadState
from tgen.common.util.base_object import BaseObject
from tgen.core.args.abstract_llm_args import AbstractLLMArgs
from tgen.core.trainers.trainer_task import TrainerTask
from tgen.models.llm.llm_responses import SupportedLLMResponses
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.tokens.token_costs import INPUT_TOKENS, ModelTokenCost, OUTPUT_TOKENS
from tgen.pipeline.state import State
from tgen.prompts.llm_prompt_build_args import LLMPromptBuildArgs

AIObject = TypeVar("AIObject")


class PromptRoles:
    USER = "user"
    ASSISTANT = "assistant"


ROLE_KEY = "role"
CONTENT_KEY = "content"


class Message(TypedDict):
    content: str
    role: str


class AbstractLLMManager(BaseObject, ABC, Generic[AIObject]):
    """
    Interface for all AI utility classes.
    """

    def __init__(self, llm_args: AbstractLLMArgs, prompt_args: LLMPromptBuildArgs, state: State = None):
        """
        Initializes the manager with args used for each request and the prompt args used for creating dataset
        :param llm_args: args used for each request
        :param prompt_args: args used for creating dataset
        :param state: The state of the pipeline.
        """
        self.llm_args = llm_args
        self.prompt_args = prompt_args
        self.state = state if state else State()

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
        completion_params = self.llm_args.to_params(TrainerTask.PREDICT, completion_type)
        completion_params.update(params)
        prompts = self.format_prompts(prompt)
        input_content = EMPTY_STRING.join([message["content"] for convo in prompts for message in convo])
        if input_content:
            self.state.total_input_cost += ModelTokenCost.calculate_cost_for_content(content=input_content,
                                                                                     model_name=self.llm_args.model,
                                                                                     input_or_output=INPUT_TOKENS,
                                                                                     raise_exception=False)

        retries = self._get_indices_to_retry(original_responses, n_expected=len(prompts))

        global_state: MultiThreadState = self.make_completion_request_impl(raise_exception=raise_exception,
                                                                           original_responses=original_responses,
                                                                           retries=retries,
                                                                           prompt=prompts,
                                                                           **completion_params)
        llm_response = global_state.results

        output_content = self.extract_all_text_from_response(llm_response)
        self.state.total_output_cost += ModelTokenCost.calculate_cost_for_content(content=output_content,
                                                                                  model_name=self.llm_args.model,
                                                                                  input_or_output=OUTPUT_TOKENS,
                                                                                  raise_exception=False)
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
    def extract_all_text_from_response(res) -> str:
        """
        Extracts all text across all batches from the response
        :param res: The response
        :return: All text across all batches from the response
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

    def make_fine_tune_request(self, completion_type: LLMCompletionType, instructions: Dict, **kwargs) -> AIObject:
        """
        Makes a fine-tuning request to LLM library.
        :param completion_type: The completion type being trained.
        :param instructions: Instructions to library parameter constructor. Not params.
        :param kwargs: Additional parameters to pass to LLM API.
        :return: Response from AI library.
        """
        params = self.llm_args.to_params(TrainerTask.TRAIN, completion_type, instructions=instructions, **kwargs)
        return self._make_fine_tune_request_impl(**params)

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

    @abstractmethod
    def _make_fine_tune_request_impl(self, **kwargs) -> AIObject:
        """
        Makes a request to fine-tune a model.
        :param completion_type: The type of task being trained on. Used to get params to API.
        :param kwargs: Named parameters to pass to AI library.
        :return: The response from AI library.
        """

    @abstractmethod
    def retrieve_fine_tune_request(self, **kwargs) -> AIObject:
        """
        Retrieves the results of a fine-tuning job.
        :param kwargs: Named parameters to pass to AI library.
        :return: The response from AI library.
        """

    @abstractmethod
    def upload_file(self, **params) -> AIObject:
        """
        Makes a request to upload a file.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """

    @classmethod
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the supported enum class for LLM args.
        :param child_class_name: The name of the child to be created.
        :return: The supported enum class.
        """
        from tgen.models.llm.supported_llm_manager import SupportedLLMManager
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
