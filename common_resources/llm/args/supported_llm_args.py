from common_resources.tools.util.supported_enum import SupportedEnum
from common_resources.llm.args.anthropic_args import AnthropicArgs
from common_resources.llm.args.open_ai_args import OpenAIArgs


class SupportedLLMArgs(SupportedEnum):
    """
    Enumerates supported language models arguments
    """
    OPENAI = OpenAIArgs
    ANTHROPIC = AnthropicArgs
