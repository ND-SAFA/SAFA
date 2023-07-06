from token import COMMA

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt

INSTRUCTION_CREATION_PROMPT = Prompt("Break the process of reverse engineering {target_type} from {source_type} into steps. "
                                     "The steps should be generalized so that they would work on any software project. "
                                     "Each step should include instructions on how to perform the step,"
                                     " a description of the expected deliverable, and a one word unique name for the step. "
                                     "The deliverable descriptions should indicate the type of information "
                                     "that would satisfy the step, rather than providing a specific example. "
                                     "The final step should be the {target_type} creation. ",
                                     PromptResponseManager(response_tag={"step":
                                                                             ["name",
                                                                              "instructions",
                                                                              "expected-deliverable-description"]},
                                                           id2tag={"step": "step", "instructions": "instructions",
                                                                   "deliverable": "expected-deliverable-description",
                                                                   "name": "name"},
                                                           response_instructions_format="Each step should be enclosed in {step} "
                                                                                        "with the instructions enclosed "
                                                                                        "in {instructions}, "
                                                                                        "a general description "
                                                                                        "of the expected deliverable "
                                                                                        "from the step enclosed in {deliverable},"
                                                                                        "and the step name enclosed in {name}."))
RELATED_ARTIFACT_PROMPT = Prompt("You are given {target_type} and a list of numbered {source_type} that may be related. "
                                 "Select the {source_type} that would be traced to the {target_type} "
                                 "and output the numbers associated with the linked {source_type} in a comma deliminated list.",
                                 response_manager=PromptResponseManager(response_tag="related-numbers",
                                                                        formatter=lambda _, val: [int(v) for v in val.split(COMMA)]))
GENERATION_PROMPT = Prompt("You are an engineering working on a software system and your goal is to reverse engineer "
                           "{source_type}s from {target_type}s. You are given a numbered list of descriptions of the "
                           "{source_type}s in the system and you must complete each step below with the "
                           "end goal of producing the {target_type}s.")
REFINE_PROMPT = Prompt("You are an engineer working on a software system "
                       "and you are are given a numbered list of descriptions of the "
                       "{source_type}s in the system as well as {target_type}s. Your goal is to refine the {target_type}s "
                       "to capture all important functionality that is specific to this system and provides meaningful information. ")
REFINE_STEP1 = QuestionPrompt("Now, identify any functionality that have not been included in the {target_type} but "
                              "are important to the system. Only functionality that is meaningful to this project should be captured. "
                              "Functionality that is true for most software systems should be excluded. "
                              "If all significant functionality has been captured, you may skip this step "
                              "and the next.",
                              response_manager=PromptResponseManager(response_tag="missing-functionality"))
REFINE_STEP2 = QuestionPrompt("Next, for any missing functionality, create a new {target_type}.",
                              response_manager=PromptResponseManager(response_tag="generate-missing"))
REFINE_STEP3 = QuestionPrompt("Then, consider if there any {target_type} that require "
                              "additional information to make them more meaningful. Output an improved version of "
                              "any {target_type}s requiring additional information. ",
                              response_manager=PromptResponseManager(response_tag="additional-info"))
REFINE_STEP4 = QuestionPrompt("Now, consider all {target_type}s. Output any {target_type} that describe functionality "
                              "that is too general "
                              "and does not provide additional information about this specific system. "
                              "If all {target_type} specify meaningful information about the system, you may skip this step. ",
                              response_manager=PromptResponseManager(response_tag="too-general"))
REFINE_STEP5 = QuestionPrompt("Using all of the previous steps, create a complete set of {target_type} for this system. "
                              "Include all of the original {target_type} that did not need improvement, "
                              "remove any that were too general, and update the list with any new ones that "
                              "capture missing functionality. Your solution should be a comma-deliminated list of the "
                              "refined {target_type}s. ",
                              response_manager=PromptResponseManager(response_tag="final-solution"))
REFINE_QUESTIONNAIRE = QuestionnairePrompt(question_prompts=[REFINE_STEP1, REFINE_STEP2, REFINE_STEP3, REFINE_STEP4, REFINE_STEP5])
