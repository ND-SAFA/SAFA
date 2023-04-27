from abc import ABC, abstractmethod
from typing import Type, List

from tgen.constants.open_ai_constants import MAX_TOKENS_DEFAULT, MAX_TOKENS_BUFFER
from tgen.data.summarizer.chunkers.open_ai_token_limits import ModelTokenLimits
from tgen.util.base_object import BaseObject
from tgen.util.override import overrides


class AbstractChunker(BaseObject, ABC):
    """
    Handles chunking for python files
    """

    def __init__(self, model_name: str, max_tokens: int = MAX_TOKENS_DEFAULT):
        """
        Initializes chunker with for a given model.
        :param model_name: The model that will be doing the tokenization
        :param max_tokens: The max number of tokens that the model can return for its completion
        :return: The approximate number of tokens
        """
        self.model_name = model_name
        self.token_limit = ModelTokenLimits.get_token_limit_for_model(self.model_name) - max_tokens - MAX_TOKENS_BUFFER

    @abstractmethod
    def chunk(self, content: str) -> List[str]:
        """
        Chunks the given content into pieces that are beneath the model's token limit
        :param content: The content to chunk
        :return: The content chunked into sizes beneath the token limit
        """

    def exceeds_token_limit(self, content: str) -> bool:
        """
        Returns true if the given content exceeds the token limit for the model.
        :param content: The content to check
        :return: True if the content exceeds the token limit for the model else False
        """
        return self.estimate_num_tokens(content, self.model_name) > self.token_limit

    @staticmethod
    def estimate_num_tokens(content: str, model_name: str) -> int:
        """
        Approximates the number of tokens that some content will be tokenized into by a given model.
        :param content: The content to be tokenized
        :param model_name: The model that will be doing the tokenization
        :return: The approximate number of tokens
        """
        return len(content.split()) * 4  # open ai's rule of thumb for approximating tokens from number of words

    @staticmethod
    def estimate_num_words_from_tokens(n_tokens: int) -> int:
        """
        Approximates the number of words that will make up the given number of tokens
        :param n_tokens: The number of tokens
        :return: The approximate number of words per n_tokens
        """
        return round(n_tokens / 4)  # open ai's rule of thumb for approximating tokens from number of words

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from tgen.data.summarizer.chunkers.supported_chunker import SupportedChunker
        return SupportedChunker
