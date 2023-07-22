from tgen.common.util.supported_enum import SupportedEnum
from tgen.core.args.anthropic_args import AnthropicArgs
from tgen.core.args.open_ai_args import OpenAIArgs


class SupportedLLMArgs(SupportedEnum):
    """
    Enumerates supported language models arguments
    """
    OPENAI = OpenAIArgs
    ANTHROPIC = AnthropicArgs
