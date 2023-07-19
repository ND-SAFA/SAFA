import re

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager, REQUIRE_ALL_TAGS
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.util.prompt_util import PromptUtil

INSTRUCTION_CREATION_PROMPT = Prompt("Imagine you are given only {source_type} from a system and you must reverse engineer "
                                     "{target_type} from the {source_type}. "
                                     "Consider what information you would need to extract from the system. "
                                     "Then construct the smallest set of only the most critical questions about "
                                     "the {source_type} that by answering would provide the most important information "
                                     "to create the {target_type}. Output the minimal set of questions in a new-line "
                                     "delimited list containing at most 10 items. ",
                                     PromptResponseManager(response_tag="questions",
                                                           required_tag_ids=REQUIRE_ALL_TAGS,
                                                           ))

DEFINITION_PROMPT = QuestionPrompt(
    "First, write a brief description of what a {target_type} is in a software development project. "
    "Focus on what differentiates this artifact from other similar software artifacts. ",
    response_manager=PromptResponseManager(response_tag="description",
                                           required_tag_ids=REQUIRE_ALL_TAGS,
                                           formatter=lambda tag, val:
                                           PromptUtil.strip_new_lines_and_extra_space(val)))
EXAMPLE_PROMPT = QuestionPrompt(
    "Then provide an example {target_type} for a software development project. The {target_type} should focus "
    "on a single feature or functionality. ",
    response_manager=PromptResponseManager(response_tag="example")
)

FORMAT_PROMPT = QuestionPrompt(
    "Finally, use your example to create a template for the typical format for an effective software development {target_type}. "
    "The template should be generalizable so it can apply to any software project and should exclude any numbering system. "
    "Include only the format. ",
    response_manager=PromptResponseManager(response_tag="format",
                                           required_tag_ids=REQUIRE_ALL_TAGS,
                                           formatter=lambda tag, val:
                                           PromptUtil.strip_new_lines_and_extra_space(val)))

FORMAT_QUESTIONNAIRE = QuestionnairePrompt(question_prompts=[DEFINITION_PROMPT, EXAMPLE_PROMPT, FORMAT_PROMPT],
                                           enumeration_chars=["-"])

GENERATION_PROMPT = Prompt("You are an engineer working on a software system and your goal is to reverse engineer "
                           "{target_type}s from {source_type}s. You are given a numbered list of descriptions of the "
                           "{source_type}s in the system below. ")
SUMMARY_INSTRUCTIONS = "Using the {source_type}, write a comprehensive summary of this system focusing on the technical details " \
                       "and design aspects needed to understand the functionality. " \
                       "In your summary, consider the following questions as guidelines to help extract useful information: "
TASK_INSTRUCTIONS = "Next, use this summary to identify the main features and functionality provided by the system. " \
                    "Then, reverse engineer a set of {target_type} that cover each of these features and functionalities. " \
                    "The {target_type} should include some technical details but " \
                    "avoid directly copying details verbatim from the {source_type}." \
                    "Importantly, the {target_type} should be specific to certain functionalities/features and not too broad. " \
                    "Do not make up any information " \
                    "- all details in the {target_type} must accurately reflect the provided {source_type}. " \
                    "{description} " \
                    "Each {target_type} should use a consistent format. Use this format as a guideline: " \
                    "{format} " \
                    "Make sure the {target_type} are concise but technically detailed, " \
                    "avoid ambiguous language, and only include information contained in the {source_type}. " \
                    "Ensure that all features and functionality are included in the {target_types}s. "

REFINE_PROMPT = Prompt("You are an engineering working on a software system and your goal is to refine "
                       "{target_type}s. You are given a summary of the system: ")
REFINE_STEPS = {
    1: QuestionPrompt("Check that each {target_type} is at the appropriate level of detail for the intended audience. "
                      "Ensure that each {target_type} contains enough context for someone unfamiliar with the system to understand, "
                      "but make sure that details are specific to this system and not contain general, uninformative details "
                      "that are true of all systems and a skilled practitioner would already know."
                      "The {target_type} should be understandable and clear to all team members. Avoid ambiguous or vague language "
                      "and do not be overly verbose. "),
    2: QuestionPrompt(
        "Ensure the {target_type} conveys only meaningful and relevant information. "
        "Details included should focus on specifics relevant to this system, "
        "rather than general information applicable to many systems. "
        "Note that the inclusion of some technical terminology does not automatically make a {target_type} system-specific. "
        "Evaluate whether the concepts are generally applicable across systems "
        "or truly specific to the design and behavior of this particular system. "
        "If any details or {target_type} are applicable across most systems remove them."),
    3: QuestionPrompt(
        "Verify there is a clear and singular purpose or goal for the {target_type}. "
        "Remove or condense any overlapping or redundant information across {target_type}s."
        "Make sure the {target_type} is independent of others, allowing work to be done in parallel."),
    4: QuestionPrompt(
        "Confirm the {target_type} is in a standard format and style consistent with the type of {target_type}."),
    5: QuestionPrompt(
        "Check that the {target_type} is technically and grammatically correct. "
        "There should be no spelling, punctuation or syntax errors."),
    6: QuestionPrompt(
        "First, for each {target_type} either provide a justification of why it already satisfies these criteria "
        "or provide what would need to be changed for it to satisfy the criteria.",
        response_manager=PromptResponseManager(response_tag="justification")),
    7: QuestionPrompt("Finally, output the revised list of the {target_type} using your justifications. "
                      "If a {target_type}s already satisfies these criteria, output the original {target_type}. "
                      "Otherwise, replace it with a refined version using your analysis. "
                      "Provide the {target_type} in the same format(s) as the originals "
                      "or remove it entirely if it is redundant or does not contain meaningful information. "
                      "The goal is to produce a streamlined set of high-quality {target_type}s with a clear and aligned purpose. "
                      "Output your list of {target_type}s in a comma-deliminated list. ",
                      response_manager=PromptResponseManager(response_tag="final-solution",
                                                             required_tag_ids=REQUIRE_ALL_TAGS))
}
REFINE_QUESTIONNAIRE = QuestionnairePrompt(instructions="Review each {target_type} carefully to ensure high quality. "
                                                        "For each {target_type}:",
                                           enumeration_chars=["-"],
                                           question_prompts=REFINE_STEPS)
