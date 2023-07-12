from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.train.args.anthropic_args import AnthropicArgs
from tgen.util.enum_util import FunctionalWrapper


class DefaultLLMManager:
    EFFICIENT = FunctionalWrapper(lambda: AnthropicManager(AnthropicArgs(model="claude-instant-v1-100k")))
    BEST = FunctionalWrapper(lambda: AnthropicManager(AnthropicArgs(model="claude-v1.3-100k")))


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
