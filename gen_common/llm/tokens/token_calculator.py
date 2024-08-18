import tiktoken

from gen_common.constants.open_ai_constants import MAX_TOKENS_BUFFER, MAX_TOKENS_DEFAULT, OPEN_AI_MODEL_DEFAULT, \
    TOKENS_2_WORDS_CONVERSION
from gen_common.llm.tokens.token_limits import ModelTokenLimits

TRUNCATE_BUFFER_WEIGHT = .25


class TokenCalculator:

    @staticmethod
    def calculate_max_prompt_tokens(model_name: str, max_completion_tokens: int = MAX_TOKENS_DEFAULT) -> int:
        """
        Gets the token limit for the given model with the given max tokens for completion
        :param model_name: The name of the model.
        :param max_completion_tokens: The max number of tokens for completion.
        :return: The token limit for any incoming prompt.
        """
        model_token_limit = ModelTokenLimits.get_token_limit_for_model(model_name)
        return model_token_limit - max_completion_tokens - MAX_TOKENS_BUFFER

    @staticmethod
    def estimate_num_tokens(content: str, model_name: str = None, is_code: bool = False) -> int:
        """
        Approximates the number of tokens that some content will be tokenized into by a given model by trying to tokenize
            and giving a rough estimate using a words to tokens conversion if that fails
        :param content: The content to be tokenized
        :param model_name: The model that will be doing the tokenization
        :param is_code: If True, assumes content is code so there are less chars per token
        :return: The approximate number of tokens
        """
        try:
            if not model_name or not ModelTokenLimits.is_open_ai_model(model_name):
                model_name = OPEN_AI_MODEL_DEFAULT  # titoken only works with open ai models so use default for approximation
            encoding = tiktoken.encoding_for_model(model_name)
            num_tokens = len(encoding.encode(content))
            if is_code:
                num_tokens = (len(content) + num_tokens) / 2  # this gives a better approx for code (less chars per token)
            return num_tokens
        except Exception:
            return TokenCalculator.rough_estimate_num_tokens(content)

    @staticmethod
    def rough_estimate_num_tokens(content: str) -> int:
        """
        Gives a rough estimate the number of tokens that some content will be tokenized into using the 4/3 rule used by open ai
        :param content: The content to be tokenized
        :return: The approximate number of tokens
        """
        return round(len(content.split()) * (1 / TOKENS_2_WORDS_CONVERSION))

    @staticmethod
    def truncate_to_fit_tokens(content: str, model_name: str = None,
                               max_completion_tokens: int = MAX_TOKENS_DEFAULT,
                               is_code: bool = True, buffer_weight: float = TRUNCATE_BUFFER_WEIGHT) -> str:
        """
        Truncates the content to fit within the token limit.
        :param content: The content to be tokenized.
        :param model_name: The name of the model.
        :param max_completion_tokens: The max number of tokens for completion.
        :param is_code: If True, assumes the content is code so higher char to token ratio.
        :param buffer_weight: The weight used to add a buffer to the number of chars to remove.
        :return: Truncated content.
        """
        n_tokens = TokenCalculator.estimate_num_tokens(content, model_name, is_code=is_code)

        max_tokens_allowed = TokenCalculator.calculate_max_prompt_tokens(model_name, max_completion_tokens)
        n_tokens_over = n_tokens - max_tokens_allowed
        if n_tokens_over <= 0:
            return content

        n_chars_over = n_tokens_over
        n_chars_over += buffer_weight * n_chars_over
        truncated_content = content[:-round(n_chars_over)]
        return truncated_content
