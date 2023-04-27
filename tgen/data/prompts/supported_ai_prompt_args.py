from tgen.data.prompts.openai_prompt_args import OpenAIPromptArgs
from tgen.util.supported_enum import SupportedEnum


class SupportedAIPromptArgs(SupportedEnum):
    """
    Enumerates the AI library's ai prompt arguments.
    """
    OPENAI = OpenAIPromptArgs
