from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from tgen.util.base_object import BaseObject
from tgen.util.llm.llm_responses import SupportedLLMResponses
from tgen.util.llm.llm_task import LLMTask

AIObject = TypeVar("AIObject")


class LLMUtil(BaseObject, ABC, Generic[AIObject]):
    """
    Interface for all AI utility classes.
    """

    @staticmethod
    @abstractmethod
    def make_fine_tune_request(**params) -> AIObject:
        """
        Makes a request to fine-tune a model.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """

    @staticmethod
    @abstractmethod
    def retrieve_fine_tune_request(**params) -> AIObject:
        """
        Retrieves the results of a fine-tuning job.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """

    @classmethod
    def make_completion_request(cls, task: LLMTask, **params) -> AIObject:
        """
        Makes a request to fine-tune a model.
        :param task: The task to translate response to.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """
        llm_response = cls.make_completion_request_impl(**params)
        return cls.translate_to_response(task, llm_response, **params)

    @staticmethod
    @abstractmethod
    def make_completion_request_impl(**params) -> AIObject:
        """
        Makes a completion request to model.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """

    @staticmethod
    @abstractmethod
    def translate_to_response(task: LLMTask, res: AIObject, **params) -> SupportedLLMResponses:
        """
        Translates the LLM library response to task specific response.
        :param task: The task to translate to.
        :param res: The response from the LLM library.
        :param params: Any additional parameters to customize translation.
        :return: A task-specific response.
        """

    @staticmethod
    @abstractmethod
    def upload_file(**params) -> AIObject:
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
        from tgen.util.llm.supported_ai_utils import SupportedLLMUtils
        return SupportedLLMUtils
