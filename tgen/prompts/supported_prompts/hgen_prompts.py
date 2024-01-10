from tgen.common.constants.deliminator_constants import COMMA, NEW_LINE
from tgen.common.constants.project_summary_constants import PS_NOTES_TAG
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.conditional_prompt import ConditionalPrompt
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
                   "\t{format}\n For example: {example} "),
    QuestionPrompt("Make sure the {target_type} are concise but technically detailed"),
    QuestionPrompt("Avoid ambiguous language, and only include information contained in the {source_type}. "),
    QuestionPrompt("Ensure that all features and functionality are included in the {target_type}s.")],
    enumeration_chars=["-"])

CLUSTERING_QUESTIONNAIRE = QuestionnairePrompt(question_prompts=[
    Prompt(
        "First you must identify the important information (e.g. features, functionality, etc.) from the {source_type}. "
        "Put this information in a section called Information. "
        "Put each unique feature, functionality or other information as its own markdown bullet. "
        f"Enclose the section in {PromptUtil.create_xml('information')}. "
        "Example:\n# Information\n  - info1\n - info2\n"),
    QuestionnairePrompt(
        instructions="Next, your primary objective is to select the information "
                     "that is relevant for the scope and purpose of {target_type}s "
                     "from that which was identified in the 'Information' section "
                     "and encapsulate it as a set of {n_targets} detailed {target_type}.",
        question_prompts=[
            QuestionPrompt("{description} "),
            QuestionnairePrompt(instructions="The {target_type} should use this format as a guideline:",
                                question_prompts=[QuestionPrompt("{format}"), QuestionPrompt("For example: {example}")],
                                enumeration_chars=["*"]),
            QuestionPrompt(
                "The {target_type}s should describe the information in the 'Information' into {n_targets} {target_type}. "
                "Group common functionality together. "
                "Use keywords and general language from the 'Information' section. "
                "Ensure that all {n_targets} {target_type} are distinct from the others. "),
            QuestionPrompt(
                "Their should be enough details to understand the functionality of the {target_type}, "
                "but each of the {n_targets} {target_type} should remain focused on a single, clear purpose. "
                "Remember to use the 'Information' section to make sure you include the appropriate details.")

        ], enumeration_chars=["-"]
    )])
SEED_PROMPT = Prompt("The above {source_type}(s) were derived from this artifact. "
                     "When creating the {target_type}(s) from {source_type}, "
                     "focus on the functionality in the {source_type} that was likely implemented/derived from it.\n\t"
                     "{seed_content}", title="Higher-level Reference Artifact")
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
REFINE_OVERVIEW_PROMPT = Prompt("You are an engineer working on a software system and your goal is to summarize "
                                "a set of {target_type}s from a software project.")
DUP_SUMMARY_TASKS = QuestionnairePrompt([
    Prompt(
        "Identify the unique features of the system mentioned in the {target_type} in detail. Focus on the key aspects of the system."
        f"Enclose your answer in {PromptUtil.create_xml('notes')} "),
    Prompt(
        "Produced a polished bulleted list detailing the unique features in the {target_type}.")],
    response_manager=PromptResponseManager(response_tag="answer"))

REFINEMENT_QUESTIONNAIRE = QuestionnairePrompt(question_prompts=[
    ConditionalPrompt(candidate_prompts=[CLUSTERING_QUESTIONNAIRE.child_prompts[0],
                                         QuestionPrompt("Cover the information in this section that is most important "
                                                        "for {target_type} in your {target_type}: "
                                                        f"{NEW_LINE}{PromptUtil.as_markdown_header('Information')}{NEW_LINE}"
                                                        "{functionality}")],
                      prompt_selector=lambda kwargs: int(kwargs.get("functionality") is not None)),
    CLUSTERING_QUESTIONNAIRE.child_prompts[1]
],
    enumeration_chars=["-"])
TITLE_PROMPT = Prompt("Create a title for the {target_type} below. "
                      "Titles should be a short identifier containing keywords describing the functionality in the {target_type}. "
                      "\nExample: User Profile Creation for Admins\n",
                      PromptResponseManager(response_tag="title", required_tag_ids=REQUIRE_ALL_TAGS)
                      )
