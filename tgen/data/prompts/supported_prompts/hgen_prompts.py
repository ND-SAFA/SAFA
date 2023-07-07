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
REFINE_STEP1 = QuestionPrompt(
    "Arrange the {target_type}s in a logical order or grouping. "
    "For example, group together all {target_type}s related to the same functionality. "
    "Output a new list of the {target_type} using this grouping. ",
    response_manager=PromptResponseManager(response_tag="grouped"))
REFINE_STEP2 = QuestionPrompt("Using your groupings and your knowledge of the system from the {source_type}, "
                              "identify if there is any missing functionality not captured in the {target_type}s. "
                              "If so add new {target_type} to capture any gaps. Output the complete list of {target_type} "
                              "including any new {target_type} created to capture missing functionality. ",
                              response_manager=PromptResponseManager(response_tag="complete"))
REFINE_STEP3 = QuestionPrompt("For each {target_type} from the previous step, "
                              "consider if they require additional details and constraints to make them more specific. "
                              "Are there details about the system that would provide useful information to the engineer "
                              "implementing the {target_type}? "
                              "You need not include any details that a skilled engineer would already know. "
                              "Include only details specific to this software project. "
                              "Output each {target_type}s, including any additional information that might be useful to it. "
                              "Leave {target_type}s that already contain sufficient information untouched. ",
                              response_manager=PromptResponseManager(response_tag="additional-info"))
REFINE_STEP4 = QuestionPrompt(
    "Review each {target_type} and eliminate any that represent generalized best practices "
    "that a skilled engineer would apply anyway. "
    "Additionally, remove any unnecessary details from the {target_type} that provide information "
    "that is common knowledge to most engineers. "
    "For example, remove any {target_type}s or details related to basic validation, security, scalability, etc. "
    "Output the updated list of {target_type}s which provide specific, meaningful information for this system.",
    response_manager=PromptResponseManager(response_tag="meaningful"))
REFINE_STEP5 = QuestionPrompt("Next, if there are any redundant {target_type}s from the previous step, eliminate them. "
                              "Multiple {target_type}s describing the same functionality "
                              "or quality attribute can be consolidated into a single, more comprehensive artifact. "
                              "Output the remaining {target_type}s which provide unique and significant information "
                              "as well as the consolidated version of any redundant {target_type}s. ",
                              response_manager=PromptResponseManager(response_tag="consolidated"))
REFINE_STEP6 = QuestionPrompt("Finally, Using all of the previous steps, review artifacts for consistency, clarity, and quality. "
                              "Refine wording and remove any ambiguity. "
                              "Output a final revised set of {target_type}s for this system. "
                              "The final {target_type} should be specific, meaningful, "
                              "and capture all significant functionality in the system. ",
                              response_manager=PromptResponseManager(response_tag="final-solution"))
REFINE_QUESTIONNAIRE = QuestionnairePrompt(question_prompts=[REFINE_STEP1, REFINE_STEP2, REFINE_STEP3,
                                                             REFINE_STEP4, REFINE_STEP5, REFINE_STEP6])
