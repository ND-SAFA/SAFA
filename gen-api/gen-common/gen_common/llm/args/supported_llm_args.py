from gen_common.llm.args.anthropic_args import AnthropicArgs
from gen_common.llm.args.open_ai_args import OpenAIArgs
from gen_common.util.supported_enum import SupportedEnum


class SupportedLLMArgs(SupportedEnum):
    """
    Enumerates supported language models arguments
    """
    OPENAI = OpenAIArgs
    ANTHROPIC = AnthropicArgs
