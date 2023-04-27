from dataclasses import dataclass

from tgen.data.prompts.args.iprompt_args import PromptArgs


@dataclass
class OpenAIPromptArgs(PromptArgs):
    """
    Defines the prompt arguments for OpenAI API.
    """
    prompt_separator = "\n\n###\n\n"
    completion_start = " "
    completion_end = "###"
