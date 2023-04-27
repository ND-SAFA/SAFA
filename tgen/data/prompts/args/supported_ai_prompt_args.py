from tgen.data.prompts.args.anthropic_prompt_args import AnthropicPromptArgs
from tgen.data.prompts.args.openai_prompt_args import OpenAIPromptArgs
from tgen.util.supported_enum import SupportedEnum


class SupportedAIPromptArgs(SupportedEnum):
    """
    Enumerates the AI library's ai prompt arguments.
    """
    OPENAI = OpenAIPromptArgs
    ANTHROPIC = AnthropicPromptArgs
