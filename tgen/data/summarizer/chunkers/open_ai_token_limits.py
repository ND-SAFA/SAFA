import string
from enum import Enum

from tgen.data.processing.cleaning.remove_unwanted_chars_step import RemoveUnwantedCharsStep


class ModelTokenLimits(Enum):
    GPT4 = 8192
    GPT432k = 32768
    GPT35turbo = 4097
    TEXTDAVINCI003 = 4096
    CODEDAVINCI = 8001
    CODECUSHMAN = 2048
    DEFAULT = 2049

    @staticmethod
    def get_token_limit_for_model(model_name: str) -> int:
        """
        Gets the token limit for a given model name
        :param model_name: The name of the model to get the limit for
        :return: The token limit
        """
        token_limit = ModelTokenLimits.DEFAULT
        model_name = RemoveUnwantedCharsStep(string.punctuation).run([model_name]).pop()
        try:
            token_limit = ModelTokenLimits[model_name.upper()]
        except KeyError:
            for mtl in ModelTokenLimits:
                if model_name in mtl.name:
                    token_limit = mtl
                    break
        return token_limit.value
