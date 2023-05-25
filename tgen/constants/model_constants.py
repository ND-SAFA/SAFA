from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.train.args.anthropic_args import AnthropicArgs

DEFAULT_LLM_MANAGER_CLS = AnthropicManager
DEFAULT_LLM_ARGS_CLS = lambda: AnthropicArgs(model="claude-instant-v1-100k")


def get_default_llm_manager() -> AbstractLLMManager:
    """
    Gets the default llm manager to use
    :return: The default llm manager
    """
    return DEFAULT_LLM_MANAGER_CLS(DEFAULT_LLM_ARGS_CLS())
