DEFAULT_RANKING_EXPLANATION_TAG = "explanation"
DEFAULT_RANKING_GOAL = (
    "\n# Goal\n"
    "You are an expert on the software project below. "
    "This software project is described under the section `Software Specification`. "
    "You are tasked with identifying which children artifacts fulfill the functionality of a single parent artifact."
    "Under the section `Software Artifacts` is the list of potential children artifacts matching the parent artifact. "
)
DEFAULT_RANKING_INSTRUCTIONS = (
    "\n\n# Instructions\n"
    "*Each questions has multiple parts, please read the instructions carefully.*"
)
QUESTION1 = (
    "Write the paragraph about the parent artifact including:"
    "\n - A description of its functionality"
    "\n - A description of what makes this artifact unique to other similar areas of the system"
    "\n - A summary of the acceptance criteria for the artifact"
    "\nUse the software specification to infer what the parent artifact is likely referring to. ",
    "parent-summary"
)

QUESTION2 = (
    "Identify the children artifacts that are related to the parent artifact's functionality. "
    "Using the format below, provide the following information for each selected child:"
    "\n    Format: ID | EXPLANATION | SCORE"
    "\n    - For `ID` provide the ID of the child currently being processed."
    "\n    - For `EXPLANATION` provide three sentences explaining:"
    "\n        1. What part of the child is relevant to the parent artifact's functionality. "
    "\n        2. How the relevant child part helps fulfill the parent artifact's functionality. "
    "\n        3. Why this child-parent connection is important to the parent artifact's functionality."
    "\n      Provide your explanation in the active voice and assume the reader is familiar with both the child and parent artifacts."
    "\n    - For `SCORE` provide a number from 1-10 representing how related the child's functionality "
    "is to the parent artifact's functionality. Use your response to (A) to know what is related to the parent artifact. "
    "Specifically, the score should be a number from 1-10. "
    "Use the following guidelines to extrapolate the correct score:"
    "\n        * 10 = Child artifact performs the parent artifact's core functionality"
    "\n        * 8 = Child performs a direct and essential function for the parent artifact"
    "\n        * 4 = Child performs an indirect function related to parent artifact"
    "\n        * 1 = Related to distant or unrelated functionality of parent artifact."
    "\nIMPORTANT: Provide each child artifact's entry on a single line. "
    "Each entry has only three components and should follow the format: ID | EXPLANATION | SCORE",
    "explanation"
)
DEFAULT_RANKING_QUESTIONS = [QUESTION1, QUESTION2]
DEFAULT_RANKING_QUERY_TAG = "parent-artifact"
