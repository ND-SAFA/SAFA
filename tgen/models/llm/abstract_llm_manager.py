from abc import ABC, abstractmethod
from typing import Dict, Generic, Type, TypeVar

from tgen.data.prompts.prompt_args import PromptArgs
from tgen.models.llm.llm_responses import SupportedLLMResponses
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.args.abstract_llm_args import AbstractLLMArgs
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.base_object import BaseObject

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

    def make_completion_request(self, completion_type: LLMCompletionType,
                                **params) -> SupportedLLMResponses:
        """
        Makes a request to fine-tune a model.
        :param completion_type: The task to translate response to.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """
        completion_params = self.llm_args.to_params(TrainerTask.PREDICT, completion_type)
        completion_params.update(params)
        llm_response = self.make_completion_request_impl(**completion_params)
        return self.translate_to_response(completion_type, llm_response, **params)

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
