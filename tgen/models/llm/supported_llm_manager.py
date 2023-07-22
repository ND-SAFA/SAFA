from tgen.common.util.supported_enum import SupportedEnum
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.open_ai_manager import OpenAIManager


class SupportedLLMManager(SupportedEnum):
    """
    Enumerates all the AI utility methods available to SAFA.
    """
    OPENAI = OpenAIManager
    ANTHROPIC = AnthropicManager
