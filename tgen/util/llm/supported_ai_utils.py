from tgen.util.llm.anthropic_util import AnthropicUtil
from tgen.util.llm.open_ai_util import OpenAIUtil
from tgen.util.supported_enum import SupportedEnum


class SupportedLLMUtils(SupportedEnum):
    """
    Enumerates all the AI utility methods available to SAFA.
    """
    OPENAI = OpenAIUtil
    ANTHROPIC = AnthropicUtil
