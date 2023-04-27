from dataclasses import dataclass


@dataclass
class PromptArgs:
    """
    Defines arguments for defining properties for prompt dataset creation.
    """
    prompt_separator: str  # Goes in between the prompt and completion
    completion_prefix: str  # Goes before the completion label during fine-tuning for classification
    completion_suffix: str  # Goes after the completion label during fine-tuning for classification
