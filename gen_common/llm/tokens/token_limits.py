from enum import Enum
from typing import Set

from gen_common.util.str_util import StrUtil


class ModelTokenLimits(Enum):
    GPT4 = 8192
    GPT432k = 32768
    GPT35TURBO = 4097
    TEXTDAVINCI003 = 4096
    CODEDAVINCI = 8001
    CODECUSHMAN = 2048
    CLAUDE = 100000  # 9216
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
        return {ModelTokenLimits.GPT4.name, ModelTokenLimits.GPT432k.name, ModelTokenLimits.GPT35TURBO.name,
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
        model_name = StrUtil.remove_punctuation(model_name).upper()
        try:
            token_limit = ModelTokenLimits[model_name.upper()]
        except KeyError:
            for mtl in ModelTokenLimits:
                if model_name in mtl.name or mtl.name in model_name:
                    token_limit = mtl
                    break
        return token_limit
