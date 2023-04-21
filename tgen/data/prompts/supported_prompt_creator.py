from enum import Enum

from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator


class SupportedPromptCreator(Enum):
    GENERATION = GenerationPromptCreator
    CLASSIFICATION = ClassificationPromptCreator
