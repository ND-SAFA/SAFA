from common_resources.tools.util.supported_enum import SupportedEnum
from common_resources.llm.anthropic_manager import AnthropicManager
from common_resources.llm.open_ai_manager import OpenAIManager


class SupportedLLMManager(SupportedEnum):
    """
    Enumerates all the AI utility methods available to SAFA.
    """
    OPENAI = OpenAIManager
    ANTHROPIC = AnthropicManager
