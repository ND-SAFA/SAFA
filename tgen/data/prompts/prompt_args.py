from dataclasses import dataclass

from tgen.data.prompts.supported_prompts import SupportedPrompts


@dataclass
class AIPromptArgs:
    """
    Defines an AI library's arguments for prompt completion.
    """
    prompt_separator: str  # Goes at the end of the prompt.
    completion_start: str  # The start of expected completion for during fine-tuning for classification.
    completion_end: str  # Goes at the end of the expected classification string during fine-tuning.


@dataclass
class PromptArgs(AIPromptArgs):
    """
    Defines arguments for defining properties for prompt dataset creation.
    """
    base_prompt: SupportedPrompts  # Defines the base prompt for the task being performed.

    def __init__(self, base_prompt: SupportedPrompts, ai_prompt_args: AIPromptArgs):
        """
        Constructs prompt args using base prompt and all arguments defined in AI prompt args.
        :param base_prompt: The base prompt to use throughout prompt creation.
        :param ai_prompt_args: The custom arguments defined per AI library.
        """
        self.base_prompt = base_prompt
        self.prompt_separator = ai_prompt_args.prompt_separator
        self.completion_start = ai_prompt_args.completion_start
        self.completion_end = ai_prompt_args.completion_end
