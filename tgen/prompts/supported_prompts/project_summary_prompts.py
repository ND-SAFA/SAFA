from tgen.common.constants.project_summary_constants import PS_DATA_FLOW_TAG, PS_DATA_FLOW_TITLE, PS_ENTITIES_TAG, PS_ENTITIES_TITLE, \
    PS_FEATURE_TAG, PS_FEATURE_TITLE, \
    PS_NOTES_TAG, PS_OVERVIEW_TAG, \
    PS_OVERVIEW_TITLE, \
    PS_SUBSYSTEM_TAG, PS_SUBSYSTEM_TITLE
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt

PROJECT_SUMMARY_SECTIONS = [
    PS_FEATURE_TITLE,
    PS_ENTITIES_TITLE,
    PS_SUBSYSTEM_TITLE,
    PS_DATA_FLOW_TITLE,
    PS_OVERVIEW_TITLE
]

PROJECT_SUMMARY_SECTIONS_DISPLAY_ORDER = [
    PS_OVERVIEW_TITLE,
    PS_FEATURE_TITLE,
    PS_ENTITIES_TITLE,
    PS_SUBSYSTEM_TITLE,
    PS_DATA_FLOW_TITLE
]

PROJECT_SUMMARY_CONTEXT_PROMPT = Prompt((
    "# Goal\n"
    "You are creating an complete document detailing the software system below."
    "The document is being created one section at a time by answering the questions at the bottom. "
    f"The goal is to read through all the artifacts and the current document progress "
    f"to accurately and exhaustively answer the questions."
))

PROJECT_SUMMARY_TAGS = {
    PS_OVERVIEW_TITLE: PS_OVERVIEW_TAG,
    PS_FEATURE_TITLE: PS_FEATURE_TAG,
    PS_ENTITIES_TITLE: PS_ENTITIES_TAG,
    PS_SUBSYSTEM_TITLE: PS_SUBSYSTEM_TAG,
    PS_DATA_FLOW_TITLE: PS_DATA_FLOW_TAG
}

PROJECT_SUMMARY_MAP = {
    PS_OVERVIEW_TITLE: QuestionnairePrompt(question_prompts=[
        QuestionPrompt("Write a set of bullet points indicating what is important in the system.",
                       response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
        QuestionPrompt("Using your notes, write a polished description of the high-level functionality of the software system. "
                       "Write in the activate voice and use 2-3 paragraphs to group your description. "
                       "Assume your reader is someone unfamiliar with the system.",
                       response_manager=PromptResponseManager(response_tag=PS_OVERVIEW_TAG))
    ]),
    PS_FEATURE_TITLE: QuestionnairePrompt(question_prompts=[
        QuestionPrompt("Make a list of all the different features present in the system.",
                       response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
        QuestionPrompt("Using your notes, list all the features of the system as formal system requirements. "
                       "Group any features that are similar into parent-child requirements. "
                       "Be as thorough as you possibly can.",
                       response_manager=PromptResponseManager(response_tag=PS_FEATURE_TAG))
    ]),
    PS_ENTITIES_TITLE: QuestionnairePrompt(question_prompts=[
        QuestionPrompt("For each feature, list all the domain entities that are needed for it.",
                       response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
        QuestionPrompt("Using your notes, create a comprehensive list of all domain entities used in the system. "
                       "Format each entity as `{name}: {description}`.",
                       response_manager=PromptResponseManager(response_tag=PS_ENTITIES_TAG))
    ]),
    PS_SUBSYSTEM_TITLE: QuestionnairePrompt(question_prompts=[
        QuestionPrompt("Create a set of sub-systems that group the similar features. "
                       "Similar features will use related domain entities and work to accomplish shared goals. "
                       "For each sub-system describe: "
                       "\n    - The functionality the sub-system."
                       "\n    - The value of the sub-system to the overall system."
                       "\n    - The software artifacts that work to implement the functionality of the sub-system"
                       "\n    - The differences to other similar sub-system in the system.",
                       response_manager=PromptResponseManager(response_tag=PS_NOTES_TAG)),
        QuestionPrompt("Using your notes, create a comprehensive description of each of the system's sub-systems.",
                       response_manager=PromptResponseManager(response_tag=PS_SUBSYSTEM_TAG,
                                                              response_instructions_format="Enclose each sub-system in {}."))
    ]),
    PS_DATA_FLOW_TITLE: QuestionnairePrompt(question_prompts=[
        QuestionPrompt("For each feature, describe:"
                       "\n    - What input data does it need?"
                       "\n    - What output data does it produce?"
                       "\n    - What features does it depend on?",
                       response_manager=PromptResponseManager(response_tag="notes")),
        QuestionPrompt(
            "Using your notes, create a polished description of how data flows throughout the system to accomplish all of its features. "
            "Use an activate voice and group your thoughts into 2-3 paragraphs.",
            response_manager=PromptResponseManager(response_tag="data-flow"))
    ])
}
