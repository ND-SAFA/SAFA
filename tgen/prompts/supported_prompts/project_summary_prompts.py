from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.common.constants.project_summary_constants import PS_DATA_FLOW_TAG, PS_ENTITIES_TAG, PS_FEATURE_TAG, PS_NOTES_TAG, \
    PS_OVERVIEW_TAG, PS_SUBSYSTEM_TAG
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt

PROJECT_SUMMARY_CONTEXT_PROMPT = Prompt((
    "# Goal\n"
    "You are creating an complete document detailing the software system below."
    "The document is being created one section at a time by answering the questions at the bottom. "
    f"The goal is to read through all the artifacts and the current document progress "
    f"to accurately and exhaustively answer the questions."
))

OVERVIEW_SECTION_PROMPT = QuestionnairePrompt(question_prompts=[
    QuestionPrompt("Write a set of bullet points indicating what is important in the system.",
                   response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
    QuestionPrompt("Using your notes, write a polished description of the high-level functionality of the software system. "
                   "Write in the activate voice and use 2-3 paragraphs to group your description. "
                   "Assume your reader is someone unfamiliar with the system.",
                   response_manager=PromptResponseManager(response_tag=PS_OVERVIEW_TAG))
])

FEATURE_SECTION_PROMPT = QuestionnairePrompt(question_prompts=[
    QuestionPrompt("Make a list of all the different features present in the system.",
                   response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
    QuestionPrompt("Using your notes, output the features of the system as formal system requirements. "
                   "Be as thorough as you possibly can.",
                   response_manager=PromptResponseManager(response_tag=PS_FEATURE_TAG,
                                                          response_instructions_format="Enclose each feature "
                                                                                       "inside of a set of {}"))
])

ENTITIES_SECTION_PROMPT = QuestionnairePrompt(question_prompts=[
    QuestionPrompt("List all the domain entities and vocabulary that are needed to understand the project.",
                   response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
    QuestionPrompt("Using your notes, create a comprehensive list of all domain entities and key vocabularly used in the system. "
                   "Format each entity as '{name}: {description}'",
                   response_manager=PromptResponseManager(response_tag=PS_ENTITIES_TAG,
                                                          response_instructions_format="and enclose each entity "
                                                                                       "inside of a set of {}"))
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
    QuestionnairePrompt(instructions="Create a set of sub-systems that group the similar features. "
                                     "Similar features will use related domain entities and work to accomplish shared goals. "
                                     "For each sub-system describe: ",
                        enumeration_chars=["-"],
                        question_prompts=[QuestionPrompt("The functionality the sub-system."),
                                          QuestionPrompt("The value of the sub-system to the overall system."),
                                          QuestionPrompt("The software artifacts that work to implement the functionality "
                                                         "of the sub-system"),
                                          QuestionPrompt("The differences to other similar sub-system in the system.")],
                        response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
    QuestionPrompt("Using your notes, create a comprehensive description of each of the system's sub-systems.",
                   response_manager=PromptResponseManager(response_tag={PS_SUBSYSTEM_TAG: ["name", "descr"]},
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
                        response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
    QuestionPrompt(
        "Using your notes, create a polished description of how data flows "
        "throughout the system to accomplish all of its features. "
        "Use an activate voice and group your thoughts into 2-3 paragraphs.",
        response_manager=PromptResponseManager(response_tag=PS_DATA_FLOW_TAG))
])
