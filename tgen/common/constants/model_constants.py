from tgen.common.util.enum_util import FunctionalWrapper
from tgen.core.args.anthropic_args import AnthropicArgs
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.open_ai_manager import OpenAIManager


class DefaultLLMManager:
    EFFICIENT = FunctionalWrapper(lambda: AnthropicManager(AnthropicArgs(model="claude-3-haiku-20240307")))
    BEST_LONG = FunctionalWrapper(lambda: AnthropicManager(AnthropicArgs(model="claude-3-sonnet-20240229")))
    BEST_SHORT = FunctionalWrapper(lambda: OpenAIManager(OpenAIArgs(model="gpt-4")))


def get_efficient_default_llm_manager() -> AbstractLLMManager:
    """
    Gets the default llm manager to use
    :return: The default llm manager
    """
    return DefaultLLMManager.EFFICIENT()


def get_best_default_llm_manager_long_context() -> AbstractLLMManager:
    """
    Gets the default llm manager to use with long contexts
    :return: The default llm manager
    """
    return DefaultLLMManager.BEST_LONG()


def get_best_default_llm_manager_short_context() -> AbstractLLMManager:
    """
    Gets the default llm manager to use with short contexts
    :return: The default llm manager
    """
    return DefaultLLMManager.BEST_SHORT()
