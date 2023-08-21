from tgen.constants.ranking_constants import DEFAULT_ARTIFACT_HEADER, PROJECT_SUMMARY_HEADER, RANKING_EXPLANATION_TAG, RANKING_ID_TAG, \
    RANKING_MAX_SCORE, \
    RANKING_PARENT_SUMMARY_TAG, RANKING_PARENT_TAG, RANKING_SCORE_TAG
from tgen.data.prompts.prompt_response_manager import PromptResponseManager

DEFAULT_RANKING_GOAL = (
    "\n# Goal\n"
    "You are an expert on the software project below. "
    f"This software project is described under `# {PROJECT_SUMMARY_HEADER}`. "
    f"You are tasked with performing software traceability for a parent artifact enclosed in <{RANKING_PARENT_TAG}></{RANKING_PARENT_TAG}> "
    f"against a list of candidate children artifacts under `# {DEFAULT_ARTIFACT_HEADER}`. "
    "Focus on identifying children artifacts that help implement the functionality of the parent artifact."
)
DEFAULT_RANKING_INSTRUCTIONS = (
    "\n\n# Instructions\n"
    "*Each questions has multiple parts, please read the instructions carefully.*"
)
QUESTION1 = (
    "Write the detailed paragraph about the parent artifact including:"
    "\n - A description of its core function and supporting sub-functions."
    "\n - A description of why this functionality is important to the users of this system."
    f"\n - A list of software artifacts that are used to achieve the parent artifact's functionality. "
    f"Use {PROJECT_SUMMARY_HEADER} to understand what artifacts are helpful to the parent."
    "\n - A description of existing functionality in the system that is related to the parent artifact's functionality."
    f"Use the information in `{PROJECT_SUMMARY_HEADER}` to understand the system the parent artifact is operating in. ",
    PromptResponseManager(response_tag=RANKING_PARENT_SUMMARY_TAG)
)

QUESTION2_INSTRUCTIONS = (
    "Enclose each artifact's exercise within {} starting with the artifact with ID 0. "
    "First, provide the ID of the artifact being processed within {}. "
    "Second, within {} provide three complete sentences answering the questions in the order below:"
    f"\n       1. What is this functionality of the child artifact? What module is the artifact a part of? Use the {PROJECT_SUMMARY_HEADER} to understand the system modules."
    "\n        2. How does the artifact's functionality help the module it is a part of?"
    "\n        3. How does the child artifact functionality affect the primary goal of the parent artifact? "
    "Use your parent summary to understand the primary goal of the parent artifact."
    "\nThird, within {} provide a score from 1-10 representing how relevant the child's functionality is to the parent artifact's functionality. "
    "Use the following guidelines to score the artifact:"
    f"\n        * {RANKING_MAX_SCORE} = Artifact performs a primary function of the parent artifact"
    "\n        * 8 = Artifact performs a supporting function to the parent artifact"
    "\n        * 6 = Artifact performs a relevant function to the parent artifact"
    "\n        * 4 = Artifact performs an indirect function related to parent artifact"
    "\n        * 1 = Related to distant or unrelated functionality of parent artifact."
    f"IMPORTANT: Make sure each artifact has three separate tags: {RANKING_ID_TAG}, {RANKING_EXPLANATION_TAG}, {RANKING_SCORE_TAG}. "
)
QUESTION2 = (
    "Below is a reasoning exercise used to determine if each artifact is a child of the parent artifact. "
    "As you work through each artifact, use your previous reasoning to reason further about the artifact. ",
    PromptResponseManager(response_instructions_format=QUESTION2_INSTRUCTIONS,
                          response_tag={"artifact": [RANKING_ID_TAG, RANKING_EXPLANATION_TAG, RANKING_SCORE_TAG]},
                          expected_response_type={"score": float, "id": int})
)

DEFAULT_RANKING_QUESTIONS = [QUESTION1, QUESTION2]
