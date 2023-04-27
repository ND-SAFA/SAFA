from enum import Enum

from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.util.supported_enum import SupportedEnum


class SupportedPromptCreator(SupportedEnum):
    GENERATION = GenerationPromptCreator
    CLASSIFICATION = ClassificationPromptCreator
