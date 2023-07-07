from copy import deepcopy
from types import DynamicClassAttribute

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.supported_prompts.classification_prompts import CLASSIFICATION_QUESTIONNAIRE
from tgen.data.prompts.supported_prompts.hgen_prompts import GENERATION_PROMPT, INSTRUCTION_CREATION_PROMPT, RELATED_ARTIFACT_PROMPT, \
    REFINE_QUESTIONNAIRE_CONTEXT, REFINE_PROMPT_CONTEXT, REFINE_QUESTIONNAIRE_ISOLATED, REFINE_PROMPT_ISOLATED
from tgen.data.prompts.supported_prompts.summary_prompts import CODE_SUMMARY, NL_SUMMARY
from tgen.util.supported_enum import SupportedEnum


class SupportedPrompts(SupportedEnum):
    HGEN_INSTRUCTIONS = INSTRUCTION_CREATION_PROMPT
    HGEN_RELATED_ARTIFACT = RELATED_ARTIFACT_PROMPT
    HGEN_GENERATION = GENERATION_PROMPT
    HGEN_REFINE_PROMPT_CONTEXT = REFINE_PROMPT_CONTEXT
    HGEN_REFINE_QUESTIONNAIRE_CONTEXT = REFINE_QUESTIONNAIRE_CONTEXT
    HGEN_REFINE_PROMPT_ISOLATED = REFINE_PROMPT_ISOLATED
    HGEN_REFINE_QUESTIONNAIRE_ISOLATED = REFINE_QUESTIONNAIRE_ISOLATED
    TGEN_CLASSIFICATION = CLASSIFICATION_QUESTIONNAIRE
    CODE_SUMMARY = CODE_SUMMARY
    NL_SUMMARY = NL_SUMMARY

    @DynamicClassAttribute
    def value(self) -> Prompt:
        """Overrides getting the value of the Enum member to return a copy."""
        return deepcopy(self._value_)
