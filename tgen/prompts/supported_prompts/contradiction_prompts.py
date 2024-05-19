from typing import List, Optional

from tgen.common.constants.deliminator_constants import COMMA
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.common_choices import CommonChoices
from tgen.contradictions.with_decision_tree.requirement import RequirementConstituent
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager, USE_ALL_TAGS
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt

CONSTITUENT2TAG = {RequirementConstituent.CONDITION: RequirementConstituent.CONDITION.value,
                   RequirementConstituent.EFFECT: RequirementConstituent.EFFECT.value,
                   RequirementConstituent.VARIABLE: {RequirementConstituent.CONDITION: f"{RequirementConstituent.CONDITION.value}-"
                                                                                       f"{RequirementConstituent.VARIABLE.value}",
                                                     RequirementConstituent.EFFECT: f"{RequirementConstituent.EFFECT.value}-"
                                                                                    f"{RequirementConstituent.VARIABLE.value}"
                                                     },
                   RequirementConstituent.ACTION: {RequirementConstituent.CONDITION: f"{RequirementConstituent.CONDITION.value}-"
                                                                                     f"{RequirementConstituent.ACTION.value}",
                                                   RequirementConstituent.EFFECT: f"{RequirementConstituent.EFFECT.value}-"
                                                                                  f"{RequirementConstituent.ACTION.value}"
                                                   }
                   }

CONDITIONS_PROMPT = Prompt("Conditions are sub-statements that are crucial for the occurrence of something else and "
                           "typically occur in subordinate clauses. "
                           "For example, for the requirement 'If the threshold is reached, then the speed must be decreased',"
                           "the condition would be *'If the threshold is reached'. "
                           "Identify if the requirement above has a condition. ",
                           response_manager=PromptResponseManager(
                               response_tag=CONSTITUENT2TAG[RequirementConstituent.CONDITION],
                               optional_tag_ids=USE_ALL_TAGS,
                               response_instructions_format="If it has a condition, output the condition enclosed in {}. "
                                                            "Otherwise, proceed to the next question."))

EFFECT_PROMPT = Prompt("Effects are the results of a condition being met. "
                       "For example, for the previous requirement example, 'the speed must be  decreased' would be the effect."
                       "It also is possible for there to be an effect "
                       "even when a condition is not explicitly included in the requirement. "
                       "For example, 'The speed must be decreased' would still be an effect even if there was no condition provided. "
                       "Identify if the requirement above has a effect.",
                       response_manager=PromptResponseManager(
                           response_tag=CONSTITUENT2TAG[RequirementConstituent.EFFECT],
                           optional_tag_ids=USE_ALL_TAGS,
                           response_instructions_format="If it has a effect, output the effect enclosed in {}. "
                                                        "Otherwise, proceed to the next question."))

VARIABLE_PROMPT = Prompt("Variables are the *subjects* of the condition and effect. "
                         "For example, the variables of 'If the threshold is reached, "
                         "the dashboard must display the speed of the car' would be "
                         "'threshold' (condition-variable) and 'dashboard' (effect-variable). "
                         "The 'speed' would NOT be a variable since the primary action is occurring on the dashboard, not the speed."
                         "There is generally exactly ONE variable in the condition (if it exists) "
                         "and exactly ONE in the effect (if it exists)."
                         "Identify the condition and effect variables in the requirement. ",
                         response_manager=PromptResponseManager(
                             response_tag=[CONSTITUENT2TAG[RequirementConstituent.VARIABLE][RequirementConstituent.CONDITION],
                                           CONSTITUENT2TAG[RequirementConstituent.VARIABLE][RequirementConstituent.EFFECT]],
                             optional_tag_ids=USE_ALL_TAGS,
                             response_instructions_format="If there is a condition with a variable, enclose it in {}. "
                                                          "If there is an effect with a variable, enclose it in {}. "))

ACTION_PROMPT = Prompt("Actions are what happens to the variables.  "
                       "For example, the actions of 'If the threshold is reached, "
                       "the dashboard must display the speed of the car and the change in velocity calculated per BR-12.' would be "
                       "'is reached' (condition-action) and 'must display' (effect-action"
                       "'calculated' would NOT be an action since it is a further description of what would be displayed, "
                       "where as 'display' WOULD BE the primary action occurring to the dashboard. "
                       "There is generally exactly ONE action in the condition (if it exists) "
                       "and exactly ONE in the effect (if it exists).",
                       response_manager=PromptResponseManager(
                           response_tag=[CONSTITUENT2TAG[RequirementConstituent.ACTION][RequirementConstituent.CONDITION],
                                         CONSTITUENT2TAG[RequirementConstituent.ACTION][RequirementConstituent.EFFECT]],
                           optional_tag_ids=USE_ALL_TAGS,
                           response_instructions_format="If there is a condition with an action, enclose it in {}. "
                                                        "If there is an effect with an action, enclose it in {}. "))

EXTRACT_CONSTITUENTS_PROMPT = QuestionnairePrompt(instructions="You must identify the condition, effect, "
                                                               "variable(s) and action(s) in the requirement if they exist.",
                                                  use_multi_step_task_instructions=True,
                                                  question_prompts=[CONDITIONS_PROMPT,
                                                                    EFFECT_PROMPT,
                                                                    VARIABLE_PROMPT,
                                                                    ACTION_PROMPT])


def format_response(tag: str, value: str) -> Optional[List[str]]:
    """
    Formats the LLM's response for the contradictions.
    :param tag: The name of the tag.
    :param value: The value of the response.
    :return: List of conflicting ids if there is a conflict, else None
    """
    conflicting_ids = value.split(COMMA)
    if len(conflicting_ids) == 1 and conflicting_ids[0].lower() == CommonChoices.NO:
        return CommonChoices.NO
    return conflicting_ids


def create_contradiction_response(explanation: str, artifact_ids: List[str]) -> str:
    """
    Creates expected LLM response format for a contradiction.
    :param explanation: Explanation of contradiction.
    :param artifact_ids: Conflicting artifact ids.
    :return: String representing format.
    """
    explanation_content = PromptUtil.create_xml(EXPLANATION_TAG, explanation)
    ids_content = PromptUtil.create_xml(CONFLICTING_IDS_TAG, COMMA.join(artifact_ids))
    tag_content = f'{explanation_content}{ids_content}'
    return PromptUtil.create_xml(CONTRADICTION_TAG, tag_content)


CONTRADICTION_TAG = "contradiction"
EXPLANATION_TAG = "explanation"
CONFLICTING_IDS_TAG = "conflicting_ids"
CONTRADICTIONS_INSTRUCTIONS = "Consider whether the following software artifact is inconsistent or contradictory with any of the " \
                              "related pieces of information. "
CONTRADICTIONS_TASK_PROMPT = QuestionnairePrompt(
    question_prompts=[Prompt("Output the ids of any contradictory or inconsistent information in a comma-deliminated list."
                             "If all the information entails or is neutral to the artifact, simply respond with no. "
                             "Otherwise, provide the conflicting ids and explanation for each contradiction found.",
                             response_manager=PromptResponseManager(response_tag={"contradiction": ["conflicting_ids", "explanation"]},
                                                                    value_formatter=format_response,
                                                                    response_instructions_format=create_contradiction_response(
                                                                        "EXPLANATION",
                                                                        ["ID1", "ID2"])))
                      ],
    use_multi_step_task_instructions=True)
