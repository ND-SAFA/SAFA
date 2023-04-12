from abc import ABC, abstractmethod
from typing import Type, List

from tgen.data.chunkers.open_ai_token_limits import ModelTokenLimits
from tgen.util.base_object import BaseObject
from tgen.util.file_util import FileUtil
from tgen.util.override import overrides


class AbstractChunker(BaseObject, ABC):
    """
    Handles chunking for python files
    """

    def __init__(self, model_name: str):
        """
        Initializes chunker with for a given model.
        :param model_name: The model that will be doing the tokenization
        :return: The approximate number of tokens
        """
        self.model_name = model_name
        self.token_limit = ModelTokenLimits.get_token_limit_for_model(self.model_name)

    def chunk(self, path_to_file: str = None, content: str = None) -> List[str]:
        """
        Chunks the given file or content into pieces that are beneath the model's token limit
        :param path_to_file: The path to the file to chunk
        :param content: The content to chunk
        :return: The content chunked into sizes beneath the token limit
        """
        content = FileUtil.read_file(path_to_file) if path_to_file else content
        assert content is not None, "No content to parse."
        return self._chunk(content)

    def exceeds_token_limit(self, content: str) -> bool:
        """
        Returns true if the given content exceeds the token limit for the model.
        :param content: The content to check
        :return: True if the content exceeds the token limit for the model else False
        """
        return self.estimate_num_tokens(content, self.model_name) > self.token_limit

    @abstractmethod
    def _chunk(self, content: str) -> List[str]:
        """
        Chunks the given content into pieces that are beneath the model's token limit
        :param content: The content to chunk
        :return: The content chunked into sizes beneath the token limit
        """

    @staticmethod
    def estimate_num_tokens(content: str, model_name: str) -> int:
        """
        Approximates the number of tokens that some content will be tokenized into by a given model.
        :param content: The content to be tokenized
        :param model_name: The model that will be doing the tokenization
        :return: The approximate number of tokens
        """
        return len(content.split()) * 4  # open ai's rule of thumb for approximating tokens from number of words

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
