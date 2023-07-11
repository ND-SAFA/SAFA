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

FORMAT_PROMPT = Prompt("Finally, provide an example of the typical format for a {target_type}. "
                       "The format should be for only the body of the {target_type} and should exclude any title.",
                       response_manager=PromptResponseManager(response_tag="format",
                                                              required_tag_ids=REQUIRE_ALL_TAGS))

REFINE_STEPS = {
    1: QuestionPrompt("Ensure the {target_type} conveys meaningful and relevant information. "
                      "The {target_type} should contain enough enough context for someone unfamiliar with the system to understand, "
                      "but details should be specific to this system and not contain details "
                      "that are true of all systems that a skilled practitioner would already know."
                      "{target_type} should be easy to read and not be overly verbose. "),
    2: QuestionPrompt(
        "Check that each {target_type} is at the appropriate level of detail for the intended audience. "
        "Remove any that do focus on general information rather than information specific to the system. "),
    3: QuestionPrompt(
        "Verify there is a clear and singular purpose or goal for the {target_type}. "
        "Remove or condense any overlapping or redundant information across {target_type}s."),
    4: QuestionPrompt(
        "Confirm the {target_type} is in a standard format and style consistent with the type of {target_type}."),
    5: QuestionPrompt(
        "Check that the {target_type} is technically and grammatically correct. "
        "There should be no spelling, punctuation or syntax errors."),
    6: QuestionPrompt("If all {target_type}s satisfy these criteria, provide the original list of {target_type}s. "
                      "Otherwise, provide a refined list of {target_type}s using your analysis. "
                      "Provide the {target_type} in the same format(s) as the originals. "
                      "The goal is to produce a streamlined set of high-quality {target_type}s with a clear and aligned purpose."
                      "Output the {target_type} in a comma-deliminated list. ",
                      response_manager=PromptResponseManager(response_tag="final-solution",
                                                             required_tag_ids=REQUIRE_ALL_TAGS))
}
REFINE_QUESTIONNAIRE = QuestionnairePrompt(instructions="Review each {target_type} carefully to ensure high quality. "
                                                        "For each {target_type}:",
                                           enumeration_chars=["-"],
                                           question_prompts=REFINE_STEPS)
