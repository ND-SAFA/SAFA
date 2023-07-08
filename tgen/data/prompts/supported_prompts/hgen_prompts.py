from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager, REQUIRE_ALL_TAGS
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt

INSTRUCTION_CREATION_PROMPT = Prompt("Break the process of reverse engineering {target_type} from {source_type} into steps. "
                                     "The steps should be generalized so that they would work on any software project, "
                                     "and the focus should be on extracting information specific to the system. "
                                     "Each step should include instructions on how to perform the step, "
                                     "a description of the expected deliverable, and a one word unique name for the step. "
                                     "The deliverable descriptions should indicate the type of information "
                                     "that would satisfy the step, rather than providing a specific example. "
                                     "Deliverables should be able to be accomplished with natural langauge alone. "
                                     "The final step should be the {target_type} creation.",
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
                                                                                        "and the step name enclosed in {name}.",
                                                           required_tag_ids=REQUIRE_ALL_TAGS))


GENERATION_PROMPT = Prompt("You are an engineering working on a software system and your goal is to reverse engineer "
                           "{target_type}s from {source_type}s. You are given a numbered list of descriptions of the "
                           "{source_type}s in the system: ")


REFINE_PROMPT_CONTEXT = Prompt("You are an engineer working on a software system "
                               "and you are are given a numbered list of descriptions of the "
                               "{source_type}s in the system as well as {target_type}s. ")
REFINE_STEP1_CONTEXT = QuestionPrompt(
    "Arrange the {target_type}s in a grouping "
    "so that {target_type} related to the same functionality or purpose are grouped together. "
    "Together each group should be focused on a single, cohesive purpose in the system. "
    "Each group should focus on a feature that represents a distinct areas of functionality and abstraction in the system design. "
    "Output a new list of the {target_type} where {target_type} focused on the same functionality are grouped together. ",
    response_manager=PromptResponseManager(response_tag="groups"))
REFINE_STEP2_CONTEXT = QuestionPrompt(
    "Using your groupings and your knowledge of the system from the summary, "
    "identify if there is any missing functionality not captured in the {target_type}s. "
    "If so add new {target_type} to capture any gaps. "
    "Output the original groupings of {target_type} "
    "and include any new {target_type} in either an existing group "
    "or a new one if it focuses on entirely different functionality. ",
    response_manager=PromptResponseManager(response_tag="complete"))
REFINE_STEP3_CONTEXT = QuestionPrompt(
    "For each group from the previous step, "
    "condense overlapping {target_type}s in the same group into a single, cohesive artifact "
    "convey the intent and functionality of each grouping. "
    "Output the condensed artifacts so that there are no overlapping artifacts. ",
    response_manager=PromptResponseManager(response_tag="condensed"))
REFINE_STEP4_CONTEXT = QuestionPrompt(
    "For each {target_type} from the previous step, "
    "consider if the information contained in them accurately reflects information from the project. "
    "Please fix any misinformation from the {target_type}s that is not consistent with the project. "
    "Output each {target_type}s, fixing any errors that you identified. ",
    response_manager=PromptResponseManager(response_tag="corrected"))
REFINE_STEP5_CONTEXT = QuestionPrompt("For each {target_type} from the previous step, "
                                      "consider if they require additional details and constraints to make them more specific. "
                                      "Are there details about the system that would provide useful information to the engineer "
                                      "implementing the {target_type}? "
                                      "You should exclude any details that are common knowledge to most engineer would already know. "
                                      "For example, do not include those related to basic validation, security, scalability, etc. "
                                      "Output each {target_type}s, including any additional information that might be useful to it. "
                                      "Leave {target_type}s that already contain sufficient information untouched. ",
                                      response_manager=PromptResponseManager(response_tag="additional-info"))
REFINE_STEP6_CONTEXT = QuestionPrompt(
    "Review each {target_type} and eliminate any that represent generalized best practices "
    "that a skilled engineer would apply anyway. "
    "Additionally, remove any unnecessary details from the {target_type} that provide information "
    "that is common knowledge to most engineers. "
    "Output the updated list of {target_type}s which provide specific, meaningful information for this system.",
    response_manager=PromptResponseManager(response_tag="meaningful"))


REFINE_PROMPT_ISOLATED = Prompt("You are an engineer working on a software system. "
                                "You are are given a list of {target_type}s pertaining to that system.")
REFINE_STEP2_ISOLATED = QuestionPrompt("Group the design requirements into the smallest set of high-level features that encompass "
                                       "related functionality. Identify the minimal number of features such that each groups "
                                       "together design requirements focused on a single, cohesive purpose in the system. "
                                       "The features should represent distinct areas of functionality and abstraction in the "
                                       "system design.",
                                       response_manager=PromptResponseManager(response_tag="groups"))

REFINE_STEP_FINAL = QuestionPrompt("Finally, output the refined {target_type}s in a comma deliminated list. "
                                   "{target_type}s should be in the same format as the original {target_types}s",
                                   response_manager=PromptResponseManager(response_tag="final-solution",
                                                                          required_tag_ids=REQUIRE_ALL_TAGS))
REFINE_QUESTIONNAIRE_CONTEXT = QuestionnairePrompt(question_prompts=[REFINE_STEP1_CONTEXT, REFINE_STEP2_CONTEXT, REFINE_STEP3_CONTEXT,
                                                                     REFINE_STEP4_CONTEXT, REFINE_STEP5_CONTEXT, REFINE_STEP6_CONTEXT,
                                                                     REFINE_STEP_FINAL])
REFINE_QUESTIONNAIRE_ISOLATED = QuestionnairePrompt(question_prompts=[# REFINE_STEP1_ISOLATED,
    REFINE_STEP2_ISOLATED,
    REFINE_STEP_FINAL])
