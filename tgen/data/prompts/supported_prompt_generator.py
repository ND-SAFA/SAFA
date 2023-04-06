from enum import Enum

from tgen.data.prompts.classification_prompt_generator import ClassificationPromptGenerator
from tgen.data.prompts.creation_prompt_generator import CreationPromptGenerator


class SupportedPromptGenerator(Enum):
    CREATION = CreationPromptGenerator
    CLASSIFICATION = ClassificationPromptGenerator
