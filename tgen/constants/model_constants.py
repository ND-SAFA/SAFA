from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.train.args.open_ai_args import OpenAIArgs

DEFAULT_LLM_MANAGER_CLS = OpenAIManager
DEFAULT_LLM_ARGS_CLS = OpenAIArgs


def get_default_llm_manager() -> AbstractLLMManager:
    """
    Gets the default llm manager to use
    :return: The default llm manager
    """
    return DEFAULT_LLM_MANAGER_CLS(DEFAULT_LLM_ARGS_CLS())
