from abc import ABC, abstractmethod
from typing import Type, List

from tgen.constants.open_ai_constants import MAX_TOKENS_DEFAULT, MAX_TOKENS_BUFFER, TOKENS_2_WORDS_CONVERSION
from tgen.data.chunkers.open_ai_token_limits import ModelTokenLimits
from tgen.util.base_object import BaseObject
from tgen.util.override import overrides
import tiktoken


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
    def chunk(self, content: str, id_: str = None) -> List[str]:
        """
        Chunks the given content into pieces that are beneath the model's token limit
        :param content: The content to chunk
        :param id_: The id associated with the content (optional)
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
        Approximates the number of tokens that some content will be tokenized into by a given model by trying to tokenize
            and giving a rough estimate using a words to tokens conversion if that fails
        :param content: The content to be tokenized
        :param model_name: The model that will be doing the tokenization
        :return: The approximate number of tokens
        """
        try:
            encoding = tiktoken.encoding_for_model(model_name)
            num_tokens = len(encoding.encode(content))
            return num_tokens
        except Exception:
            return AbstractChunker._rough_estimate_num_tokens(content)

    @staticmethod
    def _rough_estimate_num_tokens(content: str) -> int:
        """
        Gives a rough estimate the number of tokens that some content will be tokenized into using the 4/3 rule used by open ai
        :param content: The content to be tokenized
        :return: The approximate number of tokens
        """
        return round(len(content.split()) * (1 / TOKENS_2_WORDS_CONVERSION))

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from tgen.data.chunkers.supported_chunker import SupportedChunker
        return SupportedChunker
