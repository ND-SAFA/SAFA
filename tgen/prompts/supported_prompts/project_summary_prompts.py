from common_resources.tools.constants.symbol_constants import EMPTY_STRING, NEW_LINE

from tgen.common.constants.project_summary_constants import PS_DATA_FLOW_TAG, PS_ENTITIES_TAG, PS_FEATURE_TAG, PS_NOTES_TAG, \
    PS_OVERVIEW_TAG, PS_SUBSYSTEM_TAG
from common_resources.tools.util.prompt_util import PromptUtil
from tgen.prompts.prompt import Prompt
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager

PROJECT_SUMMARY_CONTEXT_PROMPT_ARTIFACTS = Prompt((
    "# Goal\n"
    "You are creating an complete document detailing the software system below."
    "The document is being created one section at a time by answering the questions at the bottom. "
    f"The goal is to read through all the artifacts and the current document progress "
    f"to accurately and exhaustively answer the questions."
))

PROJECT_SUMMARY_CONTEXT_PROMPT_VERSIONS = Prompt((
    "# Goal\n"
    "You are creating an complete document detailing the software system below."
    "The document is being created one section at a time by answering the questions at the bottom. "
    "Currently, there are several versions of this section, creating by examining different subsets of the system."
    f"The goal is to read through all the versions that have been created, condense repeated or overlapping portions, and "
    f"organize them into a cohesive final section that accurately and exhaustively answer the questions."
))

OVERVIEW_SECTION_PROMPT = QuestionnairePrompt(
    question_prompts=[
        QuestionPrompt("Write a set of bullet points indicating what is important in the system.",
                       response_manager=XMLResponseManager(response_tag=PS_NOTES_TAG)),
        QuestionPrompt("Using your notes, write a polished description of the high-level functionality of the software system. "
                       "Write in the activate voice and use 2-3 paragraphs to group your description. "
                       "Assume your reader is someone unfamiliar with the system.",
                       response_manager=XMLResponseManager(response_tag=PS_OVERVIEW_TAG))
    ])

FEATURE_SECTION_PROMPT = QuestionnairePrompt(question_prompts=[
    QuestionPrompt("Make a list of all the different features present in the system.",
                   response_manager=XMLResponseManager(response_tag=PS_NOTES_TAG)),
    QuestionPrompt("Using your notes, output the features of the system as formal system requirements. "
                   "Be as thorough as you possibly can.",
                   response_manager=XMLResponseManager(response_tag=PS_FEATURE_TAG,
                                                       response_instructions_format="Enclose each feature "
                                                                                    "inside of a set of {}",
                                                       value_formatter=lambda t, v: PromptUtil.as_bullet_point(v)))
])


def entities_formatter(t, v):
    """
    Formats the expected sub-systems section.
    :param t: Ignored.
    :param v: The dictionary mapping tag to response.
    :return: The title and description of the subsection parsed.
    """
    name_query = v["name"]
    descr_query = v["descr"]
    if len(name_query) == 0 or len(descr_query) == 0:
        return EMPTY_STRING
    formatted = PromptUtil.as_bullet_point(f"{name_query[0]}: {descr_query[0]}")
    return formatted


ENTITIES_SECTION_PROMPT = QuestionnairePrompt(question_prompts=[
    QuestionPrompt("Think about what domain entities and vocabulary that are needed to understand the project. "
                   "Write a short PARAGRAPH describing each one.",
                   response_manager=XMLResponseManager(response_tag=PS_NOTES_TAG)),
    QuestionPrompt("Using your notes, create a comprehensive list of all domain entities and key vocabularly used in the system "
                   "and use xml format to output them. ",
                   response_manager=XMLResponseManager(response_tag={PS_ENTITIES_TAG: ["name", "descr"]},
                                                       response_instructions_format="Enclose each entity in {} "
                                                                                    "with the name of the entity inside of "
                                                                                    "{} and the description inside of {}.",
                                                       entry_formatter=entities_formatter))
])


def subsection_formatter(t, v):
    """
    Formats the expected sub-systems section.
    :param t: Ignored.
    :param v: The dictionary mapping tag to response.
    :return: The title and description of the subsection parsed.
    """
    name_query = v["name"]
    descr_query = v["descr"]
    if len(name_query) == 0 or len(descr_query) == 0:
        return EMPTY_STRING
    content_items = [name_query[0], descr_query[0]]
    return NEW_LINE.join(content_items)


SUBSYSTEM_SECTION_PROMPT = QuestionnairePrompt(question_prompts=[
    QuestionnairePrompt(instructions="First you are to think about a set of sub-systems that group the similar features. "
                                     "Similar features will use related domain entities and work to accomplish shared goals. "
                                     "For each sub-system write a short paragraph that describes: ",
                        enumeration_chars=["-"],
                        question_prompts=[QuestionPrompt("The functionality the sub-system."),
                                          QuestionPrompt("The value of the sub-system to the overall system."),
                                          QuestionPrompt("The software artifacts that work to implement the functionality "
                                                         "of the sub-system"),
                                          QuestionPrompt("The differences to other similar sub-system in the system.")],
                        response_manager=XMLResponseManager(response_tag=PS_NOTES_TAG)),
    QuestionPrompt("Using your notes, create a comprehensive description of each of the system's sub-systems "
                   "and output them in xml format.",
                   response_manager=XMLResponseManager(response_tag={PS_SUBSYSTEM_TAG: ["name", "descr"]},
                                                       response_instructions_format="Enclose each sub-system in {} "
                                                                                    "with the name of the subsystem inside of "
                                                                                    "{} and the description inside of {}.",
                                                       entry_formatter=subsection_formatter))
])

DATA_FLOW_SECTION_PROMPT = QuestionnairePrompt(question_prompts=[
    QuestionnairePrompt(instructions="For each feature, describe:",
                        enumeration_chars=["-"],
                        question_prompts=[QuestionPrompt("What input data does it need?"),
                                          QuestionPrompt("What output data does it produce?"),
                                          QuestionPrompt("What features does it depend on?")],
                        response_manager=XMLResponseManager(response_tag=PS_NOTES_TAG)),
    QuestionPrompt(
        "Using your notes, create a polished description of how data flows "
        "throughout the system to accomplish all of its features. "
        "Use an activate voice and group your thoughts into 2-3 paragraphs.",
        response_manager=XMLResponseManager(response_tag=PS_DATA_FLOW_TAG))
])
