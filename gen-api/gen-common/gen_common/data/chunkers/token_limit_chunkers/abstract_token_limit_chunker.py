from abc import ABC, abstractmethod
from typing import List, Type

from gen_common.llm.tokens.token_calculator import TokenCalculator
from gen_common.infra.base_object import BaseObject
from gen_common.util.override import overrides


class AbstractTokenLimitChunker(BaseObject, ABC):
    """
    Handles chunking for python files
    """

    def __init__(self, model_name: str, max_prompt_tokens: int):
        """
        Initializes chunker with for a given model.
        :param model_name: The model that will be doing the tokenization
        :param max_prompt_tokens: The number of tokens that the model can accept
        :return: The approximate number of tokens
        """
        self.model_name = model_name
        self.max_prompt_tokens = max_prompt_tokens

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
        n_expected_tokens = TokenCalculator.estimate_num_tokens(content, self.model_name)
        return n_expected_tokens > self.max_prompt_tokens

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from gen_common.data.chunkers.token_limit_chunkers.supported_chunker import SupportedChunker
        return SupportedChunker
