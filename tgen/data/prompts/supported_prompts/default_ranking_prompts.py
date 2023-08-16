DEFAULT_RANKING_EXPLANATION_TAG = "explanation"
DEFAULT_RANKING_GOAL = (
    "\n# Goal\n"
    "You are an expert on the software project below. "
    "This software project is described under the section `Software Specification`. "
    "You are tasked with perform software traceability for a parent artifact enclosed in <parent-artifact></parent-artifact>."
    "Under the section `Software Artifacts` is the list of candidate children artifacts."
    "Focus on children artifacts that would be useful for a human analyst to consider while working on the parent artifact."
)
DEFAULT_RANKING_INSTRUCTIONS = (
    "\n\n# Instructions\n"
    "*Each questions has multiple parts, please read the instructions carefully.*"
)
QUESTION1 = (
    "Write the detailed paragraph about the parent artifact including:"
    "\n - A description of its core function and supporting sub-functions."
    "\n - A description of why this functionality is important to the users of this system."
    "\n - A description of existing functionality in the system that is related to the parent artifact's functionality."
    "Use the information in `Software Specification` to understand the system the parent artifact is operating in. ",
    "parent-summary"
)

QUESTION2 = (
    "Using the format below, provide the following information for each child:"
    "\n    Format: ID | EXPLANATION | SCORE"
    "\n    - For `ID` provide the ID of the child currently being processed."
    "\n    - For `EXPLANATION` provide three complete sentences answering the questions in the order below:"
    "\n        1. What is this functionality of the child artifact?"
    "\n        2. What is the goal of the child artifact's functionality?"
    "\n        3. How does the child artifact affect the primary goal of the parent artifact? "
    "Use your answer enclosed in <parent-summary></parent-summary to guide its importance."
    "\n      Provide your explanation in the active voice and assume the reader is familiar with both the child and parent artifacts. "
    "\n    - For `SCORE` provide a number from 1-10 representing how relevant the child's functionality is to the parent artifact's functionality. "
    "Use the following guidelines to score the child artifact:"
    "\n        * 10 = Child artifact performs a primary function of the parent artifact"
    "\n        * 8 = Child artifact performs a supporting function of the parent artifact"
    "\n        * 6 = Child artifact performs a relevant function to the parent artifact"
    "\n        * 4 = Child artifact performs an indirect function related to parent artifact"
    "\n        * 1 = Related to distant or unrelated functionality of parent artifact."
    "\nIMPORTANT: Provide each child artifact's entry on a single line. Start with the artifact with ID 0. "
    "Each entry has only three components and should follow the format: ID | EXPLANATION | SCORE. Please use `|` as the delimiter.",
    "explanation"
)
DEFAULT_RANKING_QUESTIONS = [QUESTION1, QUESTION2]
DEFAULT_RANKING_QUERY_TAG = "parent-artifact"
