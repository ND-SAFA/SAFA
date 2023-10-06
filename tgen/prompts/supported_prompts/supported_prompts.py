from copy import deepcopy
from types import DynamicClassAttribute

from tgen.common.util.supported_enum import SupportedEnum
from tgen.prompts.prompt import Prompt
from tgen.prompts.supported_prompts.artifact_summary_prompts import CODE_SUMMARY, NL_SUMMARY
from tgen.prompts.supported_prompts.classification_prompts import CLASSIFICATION_QUESTIONNAIRE
from tgen.prompts.supported_prompts.tracing_prompts import RANKING_GOAL, QUESTION1, QUESTION2, EXPLANATION_GOAL
from tgen.prompts.supported_prompts.delta_prompts import DIFF_SUMMARY_QUESTIONNAIRE, DIFF_SUMMARY_STARTER_PROMPT, \
    CHANGE_SUMMARY_STARTER_PROMPT, CHANGE_SUMMARY_QUESTIONNAIRE, IMPACTS_PROMPT, ADDED_PROMPT, DELETED_PROMPT
from tgen.prompts.supported_prompts.hgen_prompts import FORMAT_QUESTIONNAIRE, GENERATION_PROMPT, INSTRUCTION_CREATION_PROMPT, \
    REFINE_PROMPT, REFINE_TASKS, SUMMARY_QUESTIONNAIRE, GENERATATION_QUESTIONNAIRE


class SupportedPrompts(SupportedEnum):
    # ---------- HGEN ----------------
    HGEN_INSTRUCTIONS = INSTRUCTION_CREATION_PROMPT
    HGEN_GENERATION = GENERATION_PROMPT
    HGEN_GENERATION_QUESTIONNAIRE = GENERATATION_QUESTIONNAIRE
    HGEN_REFINEMENT = REFINE_PROMPT
    HGEN_REFINE_TASKS = REFINE_TASKS
    HGEN_FORMAT_QUESTIONNAIRE = FORMAT_QUESTIONNAIRE
    HGEN_SUMMARY_QUESTIONNAIRE = SUMMARY_QUESTIONNAIRE

    # ---------- TGEN ----------------
    TGEN_CLASSIFICATION = CLASSIFICATION_QUESTIONNAIRE

    # ---------- SUMMARY ----------------
    CODE_SUMMARY = CODE_SUMMARY
    NL_SUMMARY = NL_SUMMARY

    # ---------- DELTA ----------------
    DIFF_SUMMARY_QUESTIONNAIRE = DIFF_SUMMARY_QUESTIONNAIRE
    DIFF_SUMMARY_STARTER = DIFF_SUMMARY_STARTER_PROMPT
    DELTA_CHANGE_SUMMARY_STARTER = CHANGE_SUMMARY_STARTER_PROMPT
    DELTA_CHANGE_SUMMARY_QUESTIONNAIRE = CHANGE_SUMMARY_QUESTIONNAIRE
    DELTA_IMPACTS = IMPACTS_PROMPT
    DELTA_NEW_FILE = ADDED_PROMPT
    DELTA_REMOVED_FILE = DELETED_PROMPT

    # ---------- RANKING ----------------
    RANKING_GOAL_INSTRUCTIONS = RANKING_GOAL
    RANKING_QUESTION1 = QUESTION1
    RANKING_QUESTION2 = QUESTION2

    EXPLANATIONS_GOAL_INSTRUCTIONS = EXPLANATION_GOAL

    @DynamicClassAttribute
    def value(self) -> Prompt:
        """Overrides getting the value of the Enum member to return a copy."""
        return deepcopy(self._value_)
