from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.ranking_constants import PROJECT_SUMMARY_HEADER
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt

GOAL = (
    "# Goal\nBelow is the set of software artifacts of a software system. "
    f"The goal is to read through all the artifacts and create a thorough document "
    f"providing all the necessary details to hand off the project to another company."
)
INSTRUCTIONS_GOAL = (
    f"# Task\n"
    f"Below are instructions for creating the document. "
    "Include as much detail as you can. Ignore details that are generally applicable across systems. "
    f"Write the document in markdown and start the document with the header '# {PROJECT_SUMMARY_HEADER}'."
    "\n\nInstructions: "
)
OVERVIEW = QuestionPrompt("Create a sub-section called `Overview` describing the main purpose of the system.")
ENTITIES = QuestionPrompt("Create a sub-section called `Entities`. Define all the major entities in the system.")
FEATURES = QuestionPrompt("Create a sub-section called `Features` outlining the major features of the system. ")
MAJOR_COMPONENTS = QuestionPrompt(
    "Create a sub-section called `Modules`. "
    "In this high level section enumerate all the major modules in the system "
    "and give a brief descriptions of what they do for the system."
)
COMPONENTS = QuestionPrompt(
    "Under `Modules`, create sub-sections for each module in the system. "
    "For each module, create a detailed report that describes:"
    "\n    - The functionality the module."
    "\n    - The value of the module to the overall system."
    "\n    - The software artifacts that work to implement the functionality of the module"
    "\n    - The differences to other similar modules in the system."
)
DATA_FLOW = QuestionPrompt(
    "Create a sub-section called `Summary` and write a paragraph describing how "
    "the system fulfills all of its features (outlined in `Features`) using its components. "
    "Describe the interactions between modules and how data flows between them."
)
TASKS = [OVERVIEW, ENTITIES, FEATURES, MAJOR_COMPONENTS, COMPONENTS, DATA_FLOW]
TASK_QUESTIONNAIRE = QuestionnairePrompt(TASKS, instructions=f"{GOAL}{NEW_LINE}{INSTRUCTIONS_GOAL}",
                                         enumeration_chars=[str(i) for i in range(1, len(TASKS)+1)],
                                         response_manager=PromptResponseManager(response_tag="document",
                                                                                response_instructions_format="Enclose the final "
                                                                                                             "document inside of {}"))
