from tgen.constants.open_ai_constants import GENERATION_MODEL_DEFAULT
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.train.args.open_ai_args import OpenAIArgs


def get_default_llm_manager() -> AbstractLLMManager:
    """
    Gets the default llm manager to use
    :return: The default llm manager
    """
    return OpenAIManager(OpenAIArgs(model=GENERATION_MODEL_DEFAULT))
