from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.util.supported_enum import SupportedEnum


class SupportedLLMManager(SupportedEnum):
    """
    Enumerates all the AI utility methods available to SAFA.
    """
    OPENAI = OpenAIManager
    ANTHROPIC = AnthropicManager
