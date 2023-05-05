from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from tgen.data.prompts.prompt_args import PromptArgs
from tgen.train.args.abstract_llm_args import AbstractLLMArgs
from tgen.util.base_object import BaseObject
from tgen.models.llm.llm_responses import SupportedLLMResponses
from tgen.models.llm.llm_task import LLMCompletionType

AIObject = TypeVar("AIObject")


class AbstractLLMManager(BaseObject, ABC, Generic[AIObject]):
    """
    Interface for all AI utility classes.
    """

    def __init__(self, llm_args: AbstractLLMArgs, prompt_args: PromptArgs):
        """
        Initializes the manager with args used for each request and the prompt args used for creating dataset
        :param llm_args: args used for each request
        :param prompt_args: args used for creating dataset
        """
        self.llm_args = llm_args
        self.prompt_args = prompt_args

    @abstractmethod
    def make_fine_tune_request(self, **params) -> AIObject:
        """
        Makes a request to fine-tune a model.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """

    @abstractmethod
    def retrieve_fine_tune_request(self, **params) -> AIObject:
        """
        Retrieves the results of a fine-tuning job.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """

    def make_completion_request(self, task: LLMCompletionType, **params) -> AIObject:
        """
        Makes a request to fine-tune a model.
        :param task: The task to translate response to.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """
        llm_response = self.make_completion_request_impl(**params)
        return self.translate_to_response(task, llm_response, **params)

    @abstractmethod
    def make_completion_request_impl(self, **params) -> AIObject:
        """
        Makes a completion request to model.
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
