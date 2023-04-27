from abc import ABC, abstractmethod
from typing import Generic, TypeVar

AIObject = TypeVar("AIObject")


class AIUtil(ABC, Generic[AIObject]):
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

    @staticmethod
    @abstractmethod
    def make_completion_request(**params) -> AIObject:
        """
        Makes a completion request to model.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """

    @staticmethod
    @abstractmethod
    def upload_file(**params) -> AIObject:
        """
        Makes a request to upload a file.
        :param params: Named parameters to pass to AI library.
        :return: The response from AI library.
        """
