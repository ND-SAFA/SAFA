from gen_common.llm.anthropic_manager import AnthropicManager
from gen_common.llm.open_ai_manager import OpenAIManager
from gen_common.util.supported_enum import SupportedEnum


class SupportedLLMManager(SupportedEnum):
    """
    Enumerates all the AI utility methods available to SAFA.
    """
    OPENAI = OpenAIManager
    ANTHROPIC = AnthropicManager
