from copy import deepcopy
from types import DynamicClassAttribute

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.supported_prompts.hgen_prompts import INSTRUCTION_CREATION_PROMPT, RELATED_ARTIFACT_PROMPT, GENERATION_PROMPT
from tgen.util.supported_enum import SupportedEnum


class SupportedPrompts(SupportedEnum):
    HGEN_INSTRUCTIONS = INSTRUCTION_CREATION_PROMPT
    HGEN_RELATED_ARTIFACT = RELATED_ARTIFACT_PROMPT
    HGEN_GENERATION = GENERATION_PROMPT

    @DynamicClassAttribute
    def value(self) -> Prompt:
        """Overrides getting the value of the Enum member to return a copy."""
        return deepcopy(self._value_)
