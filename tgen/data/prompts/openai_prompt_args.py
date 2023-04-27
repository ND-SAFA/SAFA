from dataclasses import dataclass

from tgen.data.prompts.prompt_args import AIPromptArgs


@dataclass
class OpenAIPromptArgs(AIPromptArgs):
    """
    Defines the prompt arguments for OpenAI API.
    """
    prompt_separator = "\n\n###\n\n"
    completion_start = " "
    completion_end = "###"
