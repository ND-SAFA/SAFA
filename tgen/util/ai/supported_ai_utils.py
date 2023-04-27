from tgen.util.ai.anthropic_util import AnthropicUtil
from tgen.util.ai.open_ai_util import OpenAiUtil
from tgen.util.supported_enum import SupportedEnum


class SupportedAiUtils(SupportedEnum):
    """
    Enumerates all the AI utility methods available to SAFA.
    """
    OPENAI = OpenAiUtil
    ANTHROPIC = AnthropicUtil
