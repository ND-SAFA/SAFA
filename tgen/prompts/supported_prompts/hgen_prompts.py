from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.project_summary_constants import PS_NOTES_TAG
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.conditional_prompt import ConditionalPrompt
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.response_managers.abstract_response_manager import USE_ALL_TAGS
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager

INSTRUCTION_CREATION_PROMPT = Prompt("Imagine you are given only {source_type} from a system and you must reverse engineer "
                                     "{target_type} from the {source_type}. "
                                     "Consider what information you would need to extract from the system. "
                                     "Then construct the smallest set of only the most critical questions about "
                                     "the {source_type} that by answering would provide the most important information "
                                     "to create the {target_type}. Output the minimal set of questions in a new-line "
                                     "delimited list containing at most 10 items. ",
                                     response_manager=XMLResponseManager(response_tag="questions",
                                                                         required_tag_ids=USE_ALL_TAGS,
                                                                         ))

DEFINITION_PROMPT = QuestionPrompt(
    "First, write a brief description of what a {target_type} is in a software development project. "
    "Focus on what differentiates this artifact from other similar software artifacts. ",
    response_manager=XMLResponseManager(response_tag="description",
                                        required_tag_ids=USE_ALL_TAGS,
                                        value_formatter=lambda tag, val:
                                        PromptUtil.strip_new_lines_and_extra_space(val)))
EXAMPLE_PROMPT = QuestionPrompt(
    "Then provide an example {target_type} for a software development project. The {target_type} should focus "
    "on a single feature or functionality. ",
    response_manager=XMLResponseManager(response_tag="example")
)

FORMAT_PROMPT = QuestionPrompt(
    "Finally, use your example to create a template for the typical format for an effective software development {target_type}. "
    "The template should be generalizable so it can apply to any software project and should exclude any numbering system. "
    "Include only the format. ",
    response_manager=XMLResponseManager(response_tag="format",
                                        required_tag_ids=USE_ALL_TAGS,
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
    QuestionnairePrompt(
        question_prompts=[
            Prompt("Your first task is to construct 1-2 well written paragraphs that will guide your work in the next task. "
                   "In the paragraph, identify what is the core goal or user need addressed by all or most of the {source_type}  "
                   "as well as the action, system behavior, or information that is provided to the user "
                   "by the {source_type} to support this core goal. "
                   "Discuss how these actions relate to one another. "
                   "Provide specific details that highlight how the {source_type} "
                   "provide the user the ability to perform each of these actions, focusing on the "
                   "details that are most important for the scope and purposes of a {target_type}. "
                   "Be as specific as possible."),
            Prompt("Importantly, do not make an information up or make assumptions. "
                   "Only use information directly from the {source_type}. "
                   "You answer should be given in 1-2 cohesive, well-written paragraphs.")
        ],
        enumeration_chars=["\t"],
        response_manager=XMLResponseManager(response_tag="core-goals")),
    QuestionnairePrompt(
        instructions="Then use the actions you identified to create {n_targets} {target_type}s "
                     "When creating the {target_type} ensure that they are:",
        question_prompts=[
            QuestionPrompt(
                "Focused on the core goals and user needs identified above. "),
            QuestionPrompt(
                "Grouping related or overlapping actions across {source_type} together. "),
            QuestionnairePrompt(
                instructions="The {target_type} fits the following description:",
                question_prompts=[QuestionPrompt("{description}")],
                enumeration_chars=["*"]),
            QuestionPrompt(
                "Incorporate appropriate details from the {source_type} to ensure that the {target_type} are clear and unambiguous. "
                "Refer to the core goals section to identify details necessary to understand "
                "how the core user need / goal is being facilitated and/or what behavior is occurring. "
                "All details MUST be focused on the main goal of the {target_type}. "
                "Do NOT make up information. "
                "ALL information must be from the provided {source_type}. "),
            QuestionnairePrompt(
                instructions="The {target_type} uses this format as a guideline:",
                question_prompts=[QuestionPrompt("{format}"),
                                  QuestionPrompt("For example: {example}")],
                enumeration_chars=["*"]),
            QuestionPrompt("Importantly, EACH {target_type} should be unique from the others and focused on a clear single purpose "
                           "which is separate from all others so that "
                           "EACH {target_type} should remain focused in its specific goal. "),
            ConditionalPrompt(
                candidate_prompts=[Prompt("Create {n_targets} DISTINCT {target_type}")],
                prompt_selector=lambda kwargs: 1 - int(
                    kwargs.get("n_targets") is not None))

        ], enumeration_chars=["-"]
    )])

API_DATAFLOW_QUESTIONNAIRE = QuestionnairePrompt(
    question_prompts=[ContextPrompt(id_to_context_artifacts={}, prompt_start="# Related Code Snippets"),
                      Prompt("# TASK \n "
                             "Create a detailed summary describing what occurs during the execution of the endpoint."
                             "\n\t- The summary should detail the input, what happens inside of each step, and the output."
                             "\n\t- The functions called during the execution of the endpoint are included above. "
                             "Embed their functionality into the summary steps. "
                             "\n\nUse the following format to structure "
                             "your output\n {format}")], enumeration_chars=[NEW_LINE]
)

DB_ENTITY_SPEC_QUESTIONNAIRE = QuestionnairePrompt(
    question_prompts=[ContextPrompt(id_to_context_artifacts={}, prompt_start="# Usages of the entity"),
                      Prompt("# TASK \n "
                             "You are given the code for an entity and summaries of each code module that uses the entity. "
                             "Extract the schema from the given entity's attributes using the following format: \n{format}.\n"
                             "Please make sure that all attributes are included. "
                             "Use the usages to make sure that you understand the attributes of "
                             "the entity in the context of the system but create ONE spec ONLY for the {source_type} provided. ")],
    enumeration_chars=[NEW_LINE]
)

SEED_PROMPT = Prompt("The above {source_type}(s) were derived from this artifact. "
                     "When creating the {target_type}(s) from {source_type}, "
                     "focus on the functionality in the {source_type} that was likely implemented/derived from it.\n\t"
                     "{seed_content}", prompt_args=PromptArgs(title="Higher-level Reference Artifact"))
SUMMARY_QUESTIONNAIRE = QuestionnairePrompt(
    question_prompts=[
        QuestionPrompt(
            "Write a set of bullet points that extracts the information that would be important for creating {target_type}s.",
            response_manager=XMLResponseManager(response_tag=PS_NOTES_TAG)),
        QuestionPrompt(
            "Come up with title for the section that would encapsulate the information contained in your notes. ",
            response_manager=XMLResponseManager(response_tag="title")),
        QuestionPrompt("Using your notes, write a polished description for the section "
                       "that is specifically focused on detailing the "
                       "information necessary for the {target_type}s. "
                       "The section will not create the {target_type}s themselves "
                       "but it will be useful to the other engineers who make them.",
                       response_manager=XMLResponseManager(response_tag="new-section-body"))])
REFINE_OVERVIEW_PROMPT = Prompt("You are an engineer working on a software system and your goal is to summarize "
                                "a set of {target_type}s from a software project.")
DUP_SUMMARY_TASKS = QuestionnairePrompt([
    Prompt("Construct 1-2 well written paragraphs that summarize the shared goal of the {target_type}. "
           "Provide specific details that highlight how the {target_type} provide the user the ability "
           "to perform the shared goal. "
           "Capture details from the {target_type} that align with the specific user actions. \n"
           "You must your response in paragraph form to another engineer "
           "who does NOT have access to the {target_type}, so do NOT reference specific requirement numbers. "
           "Importantly, do not make an information up or make assumptions. "
           "Only use information directly from the {target_type}. ")],
    response_manager=XMLResponseManager(response_tag="answer"))

REFINEMENT_QUESTIONNAIRE = QuestionnairePrompt(question_prompts=[
    ConditionalPrompt(candidate_prompts=[CLUSTERING_QUESTIONNAIRE.child_prompts[0],
                                         QuestionnairePrompt(
                                             question_prompts=[Prompt("Focus on the core goals / user needs below when creating "
                                                                      "the {n_targets} {target_type}. "
                                                                      f"{NEW_LINE} CORE GOALS: "
                                                                      f"{NEW_LINE}"
                                                                      "{functionality}"
                                                                      f"{NEW_LINE}")],
                                             enumeration_chars=["!"])
                                         ],
                      prompt_selector=lambda kwargs: int(kwargs.get("functionality") is not None)),
    *CLUSTERING_QUESTIONNAIRE.child_prompts[1:]
])
TITLE_PROMPT = Prompt("Create a title for the {target_type} "
                      "that is descriptive enough to give someone unfamiliar with it a good idea of the content. "
                      "Titles should summarize the main goal of the {target_type} in the form of a concise identifier. "
                      "Try to use as much language directly from the {target_type} as possible "
                      "and keep the number of words to 5 or less PRINCIPAL words. "
                      "\nExample: Category Filtering for Product Discovery \n",
                      response_manager=XMLResponseManager(response_tag="title", required_tag_ids=USE_ALL_TAGS)
                      )
