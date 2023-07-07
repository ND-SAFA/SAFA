from copy import deepcopy
from types import DynamicClassAttribute

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.supported_prompts.classification_prompts import CLASSIFICATION_QUESTIONNAIRE
from tgen.data.prompts.supported_prompts.hgen_prompts import GENERATION_PROMPT, INSTRUCTION_CREATION_PROMPT, REFINE_PROMPT, \
    REFINE_QUESTIONNAIRE, RELATED_ARTIFACT_PROMPT
from tgen.data.prompts.supported_prompts.summary_prompts import CODE_SUMMARY, NL_SUMMARY
from tgen.util.supported_enum import SupportedEnum


class SupportedPrompts(SupportedEnum):
    HGEN_INSTRUCTIONS = INSTRUCTION_CREATION_PROMPT
    HGEN_RELATED_ARTIFACT = RELATED_ARTIFACT_PROMPT
    HGEN_GENERATION = GENERATION_PROMPT
    HGEN_REFINE_PROMPT = REFINE_PROMPT
    HGEN_REFINE_QUESTIONNAIRE = REFINE_QUESTIONNAIRE
    TGEN_CLASSIFICATION = CLASSIFICATION_QUESTIONNAIRE
    CODE_SUMMARY = CODE_SUMMARY
    NL_SUMMARY = NL_SUMMARY

    @DynamicClassAttribute
    def value(self) -> Prompt:
        """Overrides getting the value of the Enum member to return a copy."""
        return deepcopy(self._value_)
