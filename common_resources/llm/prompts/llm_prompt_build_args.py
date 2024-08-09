from dataclasses import dataclass

from common_resources.tools.constants.symbol_constants import EMPTY_STRING


@dataclass
class LLMPromptBuildArgs:
    """
    Defines arguments for defining properties for prompt dataset creation.
    """
    prompt_prefix: str = EMPTY_STRING  # Goes before the prompt.
    prompt_suffix: str = EMPTY_STRING  # Goes after the prompt.
    completion_prefix: str = EMPTY_STRING  # Goes before the completion label during fine-tuning for classification
    completion_suffix: str = EMPTY_STRING  # Goes after the completion label during fine-tuning for classification
    build_system_prompts: bool = True
