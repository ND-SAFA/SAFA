from dataclasses import dataclass

from tgen.data.prompts.args.iprompt_args import iPromptArgs


@dataclass
class AnthropicPromptArgs(iPromptArgs):
    """
    Defines prompt arguments for anthropic API.
    """
    prompt_separator = "\n\nAssistant:"
    completion_start = " "
    completion_end = "###"
