from dataclasses import dataclass

from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.train.args.ai_args import AIArgs


@dataclass
class AnthropicArgs(AIArgs):
    """
    Defines the arguments to the anthropic API.
    """
    prompt_args = PromptArgs(prompt_separator="\n\nAssistant:", completion_prefix=" ", completion_suffix="###")
    prompt_creator: AbstractPromptCreator = ClassificationPromptCreator(prompt_args=prompt_args)
