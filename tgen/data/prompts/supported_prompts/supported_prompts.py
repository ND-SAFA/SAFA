from copy import deepcopy
from types import DynamicClassAttribute

from tgen.common.util.supported_enum import SupportedEnum
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.supported_prompts.classification_prompts import CLASSIFICATION_QUESTIONNAIRE
from tgen.data.prompts.supported_prompts.hgen_prompts import FORMAT_QUESTIONNAIRE, GENERATION_PROMPT, INSTRUCTION_CREATION_PROMPT, \
    REFINE_PROMPT, REFINE_QUESTIONNAIRE
from tgen.data.prompts.supported_prompts.summary_prompts import CODE_SUMMARY, NL_SUMMARY
from tgen.delta.delta_prompts import CHANGED_FILE_PROMPT, DIFF_SUMMARY_QUESTIONNAIRE, PROJECT_SUMMARY_PROMPT


class SupportedPrompts(SupportedEnum):
    # ---------- HGEN ----------------
    HGEN_INSTRUCTIONS = INSTRUCTION_CREATION_PROMPT
    HGEN_GENERATION = GENERATION_PROMPT
    HGEN_REFINEMENT = REFINE_PROMPT
    HGEN_REFINE_QUESTIONNAIRE = REFINE_QUESTIONNAIRE
    HGEN_FORMAT_QUESTIONNAIRE = FORMAT_QUESTIONNAIRE

    # ---------- TGEN ----------------
    TGEN_CLASSIFICATION = CLASSIFICATION_QUESTIONNAIRE

    # ---------- SUMMARY ----------------
    CODE_SUMMARY = CODE_SUMMARY
    NL_SUMMARY = NL_SUMMARY

    # ---------- DELTA ----------------
    DELTA_CHANGED_FILE_PROMPT = CHANGED_FILE_PROMPT
    DELTA_DIFF_SUMMARY_QUESTIONNAIRE = DIFF_SUMMARY_QUESTIONNAIRE
    DELTA_PROJECT_SUMMARY_PROMPT = PROJECT_SUMMARY_PROMPT

    @DynamicClassAttribute
    def value(self) -> Prompt:
        """Overrides getting the value of the Enum member to return a copy."""
        return deepcopy(self._value_)
