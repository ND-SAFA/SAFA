from tgen.common.constants.deliminator_constants import COMMA
from tgen.contradictions.requirement import RequirementConstituent
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager
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
                               response_tag="condition",
                               response_instructions_format="If it has a condition, output the condition enclosed in {}. "
                                                            "Otherwise, proceed to the next question."))

EFFECT_PROMPT = Prompt("Effects are the results of a condition being met. "
                       "For example, for the previous requirement example, 'the speed must be  decreased' would be the effect."
                       "It also is possible for there to be an effect "
                       "even when a condition is not explicitly included in the requirement. "
                       "For example, 'The speed must be decreased' would still be an effect even if there was no condition provided. "
                       "Identify if the requirement above has a effect.",
                       response_manager=PromptResponseManager(
                           response_tag="effect",
                           response_instructions_format="If it has a effect, output the effect enclosed in {}. "
                                                        "Otherwise, proceed to the next question."))

VARIABLE_PROMPT = Prompt("Variables are the *subjects* of the condition and effect. "
                         "For example, the variables of 'If the threshold is reached, "
                         "the speed of the car must be decreased' would be "
                         "'threshold' and 'speed of the car'. There is generally one variable in the condition (if it exists) "
                         "and one in the effect (if it exists)."
                         "Identify any variables in the requirement. ",
                         response_manager=PromptResponseManager(
                             value_formatter=lambda tag, val: val.split(COMMA),
                             response_tag=["condition-variable", "effect-variable"],
                             response_instructions_format="If there is a condition with a variable, enclose it in {}. "
                                                          "If there is an effect with a variable, enclose it in {}. "))

ACTION_PROMPT = Prompt("Actions are what happens to the variables.  "
                       "For example, the actions of 'If the threshold is reached, the speed of the car must be decreased' would be "
                       "'is reached' and 'must be decreased'"
                       "Identify any actions in the requirement.",
                       response_manager=PromptResponseManager(
                           response_tag=["condition-action", "effect-action"],
                           value_formatter=lambda tag, val: val.split(COMMA),
                           response_instructions_format="If there is a condition with an action, enclose it in {}. "
                                                        "If there is an effect with an action, enclose it in {}. "))

EXTRACT_CONSTITUENTS_PROMPT = QuestionnairePrompt(instructions="You must identify the condition(s), effect(s), "
                                                               "variable(s) and action(s) in the requirement if they exist.",
                                                  use_multi_step_task_instructions=True,
                                                  question_prompts=[CONDITIONS_PROMPT,
                                                                    EFFECT_PROMPT,
                                                                    VARIABLE_PROMPT,
                                                                    ACTION_PROMPT])
