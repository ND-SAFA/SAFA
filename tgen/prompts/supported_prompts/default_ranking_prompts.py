from tgen.common.constants.ranking_constants import DEFAULT_ARTIFACT_HEADER, PROJECT_SUMMARY_HEADER, RANKING_ARTIFACT_TAG, \
    RANKING_EXPLANATION_TAG, \
    RANKING_ID_TAG, RANKING_MAX_SCORE, RANKING_PARENT_SUMMARY_TAG, \
    RANKING_SCORE_TAG
from tgen.common.util.prompt_util import PromptUtil

from tgen.prompts.prompt_response_manager import PromptResponseManager

DEFAULT_RANKING_GOAL = (
    f"\n{PromptUtil.format_as_markdown_header('Goal')}\n"
    "You are an expert on the software project below. "
    f"This software project is described under `{PromptUtil.format_as_markdown_header(PROJECT_SUMMARY_HEADER)}`. "
    f"You are tasked with performing software traceability for a parent artifact (enclosed in {PromptUtil.create_xml(RANKING_ARTIFACT_TAG)}) "
    f"against a list of candidate children artifacts under `{PromptUtil.format_as_markdown_header(DEFAULT_ARTIFACT_HEADER)}`. "
    "The children have been selected for being similar to the parent, however, there are many false positives. "
    "You're job is to distinguish the artifacts that are truly relevant to the parent's functionality by "
    "focusing on understanding the children artifacts in the context of the system to help achieve this goal."
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

SCORE_INSTRUCTIONS = (
    "provide a score from 1-10 representing how relevant the child's functionality is to the parent artifact's functionality. "
    "Use the following guidelines to score the artifact:"
    f"\n        * {RANKING_MAX_SCORE} = Artifact performs a primary function of the parent artifact"
    "\n        * 8 = Artifact performs a supporting function to the parent artifact"
    "\n        * 6 = Artifact performs a relevant function to the parent artifact"
    "\n        * 4 = Artifact performs an indirect function related to parent artifact"
    "\n        * 1 = Related to distant or unrelated functionality of parent artifact."
)

QUESTION2_INSTRUCTIONS = (
        "Starting with artifact ID 0, answer the following questions for each artifact within {}"
        "\n    1. Provide the ID of the artifact being processed within {}. "
        "\n    2. Within {} provide three complete sentences answering the questions in the order below:"
        f"\n        A. What is this functionality of the child artifact? What module is the artifact a part of? Use the {PROJECT_SUMMARY_HEADER} to understand the system modules."
        "\n        B. How does the artifact's functionality help the module it is a part of?"
        "\n        C. How does the child artifact functionality affect the primary goal of the parent artifact? "
        "Use your parent summary to understand the primary goal of the parent artifact."
        "\n    3. within {}" + f" {SCORE_INSTRUCTIONS}" +
        f"IMPORTANT: Make sure there are three separate tags "
        f"({RANKING_ID_TAG}, {RANKING_EXPLANATION_TAG}, {RANKING_SCORE_TAG}) within {PromptUtil.create_xml(RANKING_ARTIFACT_TAG)}."
)
QUESTION2 = (
    "Below is a set of reasoning steps used to determine if each artifact is a child of the parent artifact. "
    "As you work through each artifact, use your previous reasoning to reason further about the artifact. ",
    PromptResponseManager(response_instructions_format=QUESTION2_INSTRUCTIONS,
                          response_tag={RANKING_ARTIFACT_TAG: [RANKING_ID_TAG, RANKING_EXPLANATION_TAG, RANKING_SCORE_TAG]},
                          expected_response_type={RANKING_SCORE_TAG: float, RANKING_ID_TAG: int})
)

DEFAULT_RANKING_QUESTIONS = [QUESTION1, QUESTION2]
