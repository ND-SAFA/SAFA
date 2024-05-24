from datetime import datetime
from enum import Enum

from tgen.common.constants.deliminator_constants import DASH, UNDERSCORE
from tgen.common.logging.logger_manager import logger
from tgen.common.util.str_util import StrUtil
from tgen.models.tokens.token_calculator import TokenCalculator

INPUT_TOKENS = 0
OUTPUT_TOKENS = 1
N_TOKENS_PER_COST = 1000


class ModelTokenCost(Enum):
    # using format ($ per input, $ per output) per 1k tokens for each of the models
    GPT_4 = (0.03, 0.06)
    GPT_4_32k = (0.06, 0.12)
    GPT_4_1106_PREVIEW = (0.01, 0.03)
    GPT_4_1106_VISION_PREVIEW = (0.01, 0.03)
    CLAUDE_INSTANT_1 = (0.00163, 0.00551)
    CLAUDE_2 = (0.01102, 0.03268)
    CLAUDE_3_HAIKU = (0.00025, 0.00125)
    CLAUDE_3_SONNET = (0.003, 0.015)
    CLAUDE_3_OPUS = (0.0015, 0.075)

    @classmethod
    def calculate_cost_for_content(cls, content: str, model_name: str, input_or_output: int = INPUT_TOKENS,
                                   raise_exception: bool = False) -> float:
        """
        Calculates the cost of the content for a given model
        :param content: The content to calculate the cost for
        :param model_name: The model to calculate the cost for
        :param input_or_output: Determines whether the content is input or output which affects cost
        :param raise_exception: If True, raises an exception on failure, otherwise just logs it
        :return: The cost of the content for a given model
         """
        n_tokens = TokenCalculator.estimate_num_tokens(content, model_name)
        return cls.calculate_cost_for_tokens(n_tokens, model_name, input_or_output, raise_exception)

    @classmethod
    def calculate_cost_for_tokens(cls, n_tokens: int, model_name: str, input_or_output: int = INPUT_TOKENS,
                                  raise_exception: bool = False) -> float:
        """
        Calculates the cost of the tokens for a given model
        :param n_tokens: The number of tokens
        :param model_name: The model to calculate the cost for
        :param input_or_output: Determines whether the tokens are input or output which affects cost
        :param raise_exception: If True, raises an exception on failure, otherwise just logs it
        :return: The cost of the tokens for a given model
        """
        try:
            cost = cls.find_token_cost_for_model(model_name)[input_or_output]
            return (n_tokens / N_TOKENS_PER_COST) * cost
        except Exception as e:
            if raise_exception:
                raise e
            logger.warning(e)
        return 0

    @classmethod
    def find_token_cost_for_model(cls, model_name: str) -> "ModelTokenLimits":
        """
        Gets the token cos for a given model name
        :param model_name: The name of the model to get the limit for
        :return: The token limit
        """
        # get main model version (e.g. claude-instant-1.2 -> claude-instant-1)
        processed_model_name = StrUtil.remove_decimal_points_from_floats(model_name)
        processed_model_name = processed_model_name.replace(DASH, UNDERSCORE)
        split_name = processed_model_name.split(UNDERSCORE)
        if split_name[-1].startswith(str(datetime.today().year)):
            processed_model_name = UNDERSCORE.join(split_name[:-1])
        try:
            return cls[processed_model_name.upper()].value
        except KeyError:
            raise KeyError(f"Unable to determine token cost: Unknown model name {model_name}")
