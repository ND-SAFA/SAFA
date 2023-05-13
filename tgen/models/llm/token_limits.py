import string
from enum import Enum

from typing import Set

from tgen.constants.open_ai_constants import MAX_TOKENS_DEFAULT, MAX_TOKENS_BUFFER, TOKENS_2_WORDS_CONVERSION, OPEN_AI_MODEL_DEFAULT
from tgen.data.processing.cleaning.remove_unwanted_chars_step import RemoveUnwantedCharsStep
import tiktoken


class ModelTokenLimits(Enum):
    GPT4 = 8192
    GPT432k = 32768
    GPT35turbo = 4097
    TEXTDAVINCI003 = 4096
    CODEDAVINCI = 8001
    CODECUSHMAN = 2048
    CLAUDE = 100000
    DEFAULT = 2049

    @staticmethod
    def is_open_ai_model(model_name: str) -> bool:
        """
        Determines if the given model is an open-ai model
        :param model_name: The name of the model
        :return: True if the model is an open-ai model else False
        """
        model = ModelTokenLimits._find_token_limit_for_model(model_name).name
        return model in ModelTokenLimits.get_open_ai_models()

    @staticmethod
    def get_open_ai_models() -> Set[str]:
        """
        Gets the set of open ai models contained in ModelTokenLimits
        :return: The set of open ai models contained in ModelTokenLimits
        """
        return {ModelTokenLimits.GPT4.name, ModelTokenLimits.GPT432k.name, ModelTokenLimits.GPT35turbo.name,
                ModelTokenLimits.TEXTDAVINCI003.name, ModelTokenLimits.CODECUSHMAN.name, ModelTokenLimits.CODEDAVINCI.name}

    @staticmethod
    def get_token_limit_for_model(model_name: str) -> int:
        """
        Gets the token limit for a given model name
        :param model_name: The name of the model to get the limit for
        :return: The token limit
        """
        token_limit = ModelTokenLimits._find_token_limit_for_model(model_name)
        return token_limit.value

    @staticmethod
    def _find_token_limit_for_model(model_name: str) -> "ModelTokenLimits":
        """
        Gets the token limit for a given model name
        :param model_name: The name of the model to get the limit for
        :return: The token limit
        """
        token_limit = ModelTokenLimits.DEFAULT
        model_name = RemoveUnwantedCharsStep(string.punctuation).run([model_name]).pop().upper()
        try:
            token_limit = ModelTokenLimits[model_name.upper()]
        except KeyError:
            for mtl in ModelTokenLimits:
                if model_name in mtl.name or mtl.name in model_name:
                    token_limit = mtl
                    break
        return token_limit


class TokenLimitCalculator:

    @staticmethod
    def calculate_token_limit(model_name: str, max_tokens: int = MAX_TOKENS_DEFAULT) -> int:
        """
        Gets the token limit for the given model with the given max tokens for completion
        :param model_name: The name of the model
        :param max_tokens: The max number of tokens for completion
        :return: The token limit
        """
        return ModelTokenLimits.get_token_limit_for_model(model_name) - max_tokens - MAX_TOKENS_BUFFER

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
            if not ModelTokenLimits.is_open_ai_model(model_name):
                model_name = OPEN_AI_MODEL_DEFAULT  # titoken only works with open ai models so use default for approximation
            encoding = tiktoken.encoding_for_model(model_name)
            num_tokens = len(encoding.encode(content))
            return num_tokens
        except Exception:
            return TokenLimitCalculator.rough_estimate_num_tokens(content)

    @staticmethod
    def rough_estimate_num_tokens(content: str) -> int:
        """
        Gives a rough estimate the number of tokens that some content will be tokenized into using the 4/3 rule used by open ai
        :param content: The content to be tokenized
        :return: The approximate number of tokens
        """
        return round(len(content.split()) * (1 / TOKENS_2_WORDS_CONVERSION))
