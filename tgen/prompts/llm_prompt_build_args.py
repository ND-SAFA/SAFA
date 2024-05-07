from dataclasses import dataclass


@dataclass
class LLMPromptBuildArgs:
    """
    Defines arguments for defining properties for prompt dataset creation.
    """
    prompt_prefix: str  # Goes before the prompt.
    prompt_suffix: str  # Goes after the prompt.
    completion_prefix: str  # Goes before the completion label during fine-tuning for classification
    completion_suffix: str  # Goes after the completion label during fine-tuning for classification
    build_system_prompts: bool
