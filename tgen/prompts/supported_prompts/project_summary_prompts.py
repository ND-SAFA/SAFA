from tgen.common.constants.tracing.ranking_constants import PROJECT_SUMMARY_HEADER
from tgen.prompts.question_prompt import QuestionPrompt

GOAL = (
    "# Goal\nBelow is the set of software artifacts of a software system. "
    f"The goal is to read through all the artifacts and create an exhaustive document "
    f"providing all the necessary details to hand off the project to another company."
)
INSTRUCTIONS_GOAL = (
    f"# Task\n"
    f"Below are instructions for creating the document. "
    "Include as much detail as you can. Ignore details that are generally applicable across systems. "
    f"Write the document in markdown and start the document with the header '# {PROJECT_SUMMARY_HEADER}'."
    "\n\nInstructions: "
)
OVERVIEW = ("Overview", QuestionPrompt("Describe the main purpose of the system."))
FEATURES = ("Features", QuestionPrompt("Outline all the features of the system. "))
ENTITIES = ("Entities", QuestionPrompt("Define all the entities in the system."))

MAJOR_COMPONENTS = ("Modules", QuestionPrompt(
    "Enumerate all the major modules in the system and give a brief descriptions of what they do for the system."
))
MODULES = ("Modules", QuestionPrompt(
    "Create a section for each module in the system detailing:"
    "\n    - The functionality the module."
    "\n    - The value of the module to the overall system."
    "\n    - The software artifacts that work to implement the functionality of the module"
    "\n    - The differences to other similar modules in the system."
))
DATA_FLOW = ("Data Flow", QuestionPrompt(
    "Write a paragraph describing how the system fulfills all of its features (outlined in `Features`) using its components. "
    "Describe the interactions between modules and how data flows between them."
))
PROJECT_SUMMARY_TASKS = [OVERVIEW, FEATURES, ENTITIES, MAJOR_COMPONENTS, MODULES, DATA_FLOW]
PROJECT_SUMMARY_SECTIONS = [s[0] for s in PROJECT_SUMMARY_TASKS]
