from tgen.common.util.enum_util import FunctionalWrapper
from tgen.core.args.anthropic_args import AnthropicArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager


class DefaultLLMManager:
    EFFICIENT = FunctionalWrapper(lambda: AnthropicManager(AnthropicArgs(model="claude-instant-1.1")))
    BEST = FunctionalWrapper(lambda: AnthropicManager(AnthropicArgs(model="claude-2.0")))


def get_efficient_default_llm_manager() -> AbstractLLMManager:
    """
    Gets the default llm manager to use
    :return: The default llm manager
    """
    return DefaultLLMManager.EFFICIENT()


def get_best_default_llm_manager() -> AbstractLLMManager:
    """
    Gets the default llm manager to use
    :return: The default llm manager
    """
    return DefaultLLMManager.BEST()
