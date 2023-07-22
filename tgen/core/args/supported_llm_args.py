from tgen.train.args.anthropic_args import AnthropicArgs
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.util.supported_enum import SupportedEnum


class SupportedLLMArgs(SupportedEnum):
    """
    Enumerates supported language models arguments
    """
    OPENAI = OpenAIArgs
    ANTHROPIC = AnthropicArgs
