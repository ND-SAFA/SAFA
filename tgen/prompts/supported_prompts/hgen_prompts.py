from tgen.common.constants.deliminator_constants import COMMA, NEW_LINE
from tgen.common.constants.project_summary_constants import PS_NOTES_TAG
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager, REQUIRE_ALL_TAGS
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt

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
                                           value_formatter=lambda tag, val:
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
                                           value_formatter=lambda tag, val:
                                           PromptUtil.strip_new_lines_and_extra_space(val)))

FORMAT_QUESTIONNAIRE = QuestionnairePrompt(question_prompts=[DEFINITION_PROMPT, EXAMPLE_PROMPT, FORMAT_PROMPT],
                                           enumeration_chars=["-"])

GENERATION_PROMPT = Prompt("You are an engineer working on a software system and your goal is to reverse engineer "
                           "{target_type}s from {source_type}s. You are given a list of ids and descriptions of the "
                           "{source_type}s in the system below. ")
SUMMARY_INSTRUCTIONS = "Using the {source_type}, write a comprehensive summary of this system focusing on the technical details " \
                       "and design aspects needed to understand the functionality. " \
                       "In your summary, consider the following questions as guidelines to help extract useful information: "

GENERATATION_QUESTIONNAIRE = QuestionnairePrompt(question_prompts=[
    QuestionPrompt("Identify the main features and functionality provided by the {source_type} and system summary. "),
    QuestionPrompt("Then, reverse engineer a set of {target_type} "
                   "that cover each of these features and functionalities. "),
    QuestionPrompt("The {target_type} should include some technical details "
                   "but avoid directly copying details verbatim from the {source_type}. "),
    QuestionPrompt("Importantly, the {target_type} should be specific to certain functionalities/features and not too broad. "),
    QuestionPrompt("Do not make up any information "
                   "- all details in the {target_type} must accurately reflect the provided {source_type}. "),
    QuestionPrompt("{description} "),
    QuestionPrompt("Each {target_type} should use a consistent format. Use this format as a guideline: "
                   "{format} "),
    QuestionPrompt("Make sure the {target_type} are concise but technically detailed"),
    QuestionPrompt("Avoid ambiguous language, and only include information contained in the {source_type}. "),
    QuestionPrompt("Ensure that all features and functionality are included in the {target_type}s.")],
    enumeration_chars=["-"])

CLUSTERING_QUESTIONNAIRE = QuestionnairePrompt(question_prompts=[
    Prompt(
        "First, write a highly detailed paragraph describing the functionality of the {source_type}(s) that should be captured by the {target_type}(s).",
        response_manager=PromptResponseManager(response_tag="notes")
    ),
    QuestionPrompt(
        "For your next task, the primary objective is to create a minimal set ({n_targets}) of detailed {target_type}s "
        "specifying the functionality achieved by the {source_type}s."
    ),
    QuestionPrompt(
        "The {target_type}s should generalize the important functionality into {n_targets} {target_type}(s). "
        "Each {target_type} should be detailed and focused on a single, clear purpose. "
        "Their should be enough details to guide the implementation of the {target_type}. "
        "Use the `Overview of System` to understand the greater context of the system containing the {source_type}s."
    ),
    QuestionPrompt("{description} "),
    QuestionPrompt("The {target_type} should use this format as a guideline: \n{format}.")
], enumeration_chars=["-"])

REFINE_PROMPT = Prompt("You are an engineer that is an expert on a software system and your goal is to refine "
                       "{target_type}s. There are many duplicate {target_type} between the new and original {target_type}s "
                       "so you must minimize the number of duplicates and select only the best artifacts to remain. "
                       "You are given a summary of the system: ")
REFINE_STEPS = {
    1: QuestionPrompt("Compare each version of {target_type}s to identify duplicates and overlaps. "
                      "Only some of the {target_type} are overlapping, and some new functionality has been introduced in each version."
                      "Two {target_type} overlap if they describe substantially the same feature or functionality. "),
    2: QuestionPrompt("Create a set of unique {target_type}s that describe unique functionality "
                      "and do NOT have significant overlap in their descriptions with the other {target_type}s."),
    3: QuestionnairePrompt(instructions="When duplicate/overlapping {target_type}s"
                                        " are found, choose the best version to keep using these criteria:",
                           question_prompts=[QuestionPrompt("Most complete and detailed description"),
                                             QuestionPrompt("Clearer articulation of the desired functionality")],
                           enumeration_chars=["*"]),
    4: QuestionnairePrompt(instructions="Consolidate the {target_type}s into a master list "
                                        "containing only the selected best versions. "
                                        "The consolidated list should have:",
                           question_prompts=[QuestionPrompt("No redundant or overlapping {target_type}s"),
                                             QuestionPrompt("ALL unique functionality represented across both versions")],
                           enumeration_chars=["*"]),
    5: QuestionPrompt("Map and document where duplicates were found and the selection rationale. "
                      "Add comments explaining the elimination decisions. "
                      "Add comments explaining why remaining {target_type}s are unique. ",
                      response_manager=PromptResponseManager(response_tag="notes")),
    6: QuestionPrompt("Output just the {target_type} numbers for the refined list in the specified format:"
                      f"{NEW_LINE}{PromptUtil.indent_for_markdown('* Comma delimited numbers')}",
                      response_manager=PromptResponseManager(response_tag="selected-artifacts",
                                                             response_instructions_format=f"{NEW_LINE}"
                                                                                          f"{PromptUtil.indent_for_markdown('* Enclosed in {} XML tags.')}",
                                                             expected_response_type=int,
                                                             value_formatter=lambda tag, val: [v.strip().strip(NEW_LINE)
                                                                                               for v in val.split(COMMA)])
                      )

}
REFINE_TASKS = QuestionnairePrompt(instructions="Carefully review the v1 and v2 {target_type} lists. "
                                                "Make sure you understand each one.",
                                   enumeration_chars=["-"],
                                   question_prompts=REFINE_STEPS)

SUMMARY_QUESTIONNAIRE = QuestionnairePrompt(
    question_prompts=[
        QuestionPrompt(
            "Write a set of bullet points that extracts the information that would be important for creating {target_type}s.",
            response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
        QuestionPrompt(
            "Come up with title for the section that would encapsulate the information contained in your notes. ",
            response_manager=PromptResponseManager(response_tag="title")),
        QuestionPrompt("Using your notes, write a polished description for the section "
                       "that is specifically focused on detailing the "
                       "information necessary for the {target_type}s. "
                       "The section will not create the {target_type}s themselves "
                       "but it will be useful to the other engineers who make them.",
                       response_manager=PromptResponseManager(response_tag="new-section-body"))])
