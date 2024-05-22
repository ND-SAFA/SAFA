from math import floor

from tgen.common.constants.deliminator_constants import L_CARROT, R_CARROT
from tgen.common.constants.ranking_constants import PROJECT_SUMMARY_HEADER, RANKING_ARTIFACT_TAG, \
    RANKING_ID_TAG, RANKING_MAX_SCORE, RANKING_PARENT_SUMMARY_TAG, \
    RANKING_SCORE_TAG, RANKING_MIN_SCORE, ARTIFACT_HEADER, RANKING_EXPLANATION_TAG, DEFAULT_SCORE
from tgen.common.util.prompt_util import PromptUtil
from tgen.common.util.str_util import StrUtil
from tgen.prompts.prompt import Prompt
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager
from tgen.prompts.select_question_prompt import SelectQuestionPrompt

RANKING_GOAL = Prompt(
    f"\n{PromptUtil.as_markdown_header('Goal')}\n"
    "You are an expert on the software project below. "
    f"This software project is described under `{PromptUtil.as_markdown_header(PROJECT_SUMMARY_HEADER)}`. "
    f"You are tasked with performing software traceability for a parent artifact "
    f"(enclosed in {PromptUtil.create_xml(RANKING_ARTIFACT_TAG)}) "
    f"against a list of candidate children artifacts under `{PromptUtil.as_markdown_header(ARTIFACT_HEADER)}`. "
    "The children have been selected for being similar to the parent, however, there are many false positives. "
    "You're job is to distinguish the artifacts that are truly relevant to the parent's functionality by "
    "focusing on understanding the children artifacts in the context of the system to help achieve this goal."
)

QUESTION1 = QuestionnairePrompt(
    instructions="FIRST, Write the detailed paragraph about the parent artifact including:",
    enumeration_chars=["-"],
    question_prompts=[QuestionPrompt("A description of its core function and supporting sub-functions."),
                      QuestionPrompt("A description of why this functionality is important to the users of this system."),
                      QuestionPrompt("A list of software artifacts that are used to achieve the parent artifact's functionality."),
                      QuestionPrompt(f"Use {PROJECT_SUMMARY_HEADER} to understand what artifacts are helpful to the parent."),
                      QuestionPrompt(
                          f"A description of existing functionality in the system "
                          f"that is related to the parent artifact's functionality. "
                          f"Use the information in `{PROJECT_SUMMARY_HEADER}` "
                          f"to understand the system the parent artifact is operating in.")
                      ], response_manager=XMLResponseManager(response_tag=RANKING_PARENT_SUMMARY_TAG))
RANKING_CATEGORIES = ["Artifacts have closely-tied functionality "
                      "or a direct design/inheritance relationship (definite trace-link) ",
                      "Artifacts support key functions of the other "
                      "or share significant similarities with only minor inconsistencies (likely trace-link) ",
                      "Portions of the artifacts have clear and direct linkage but other portions are unrelated (possible trace-link)",
                      "Partial topical overlap. The artifacts have some loosely related content "
                      "but differences outweigh the similarities (unsure if trace-link) ",
                      "Vague or abstract similarity. "
                      "The artifacts hare only very high-level topics or broad concepts but no specifics (weak trace-link) ",
                      "No discernible relationship between artifacts can be identified ",
                      "No discernible relationship between artifacts can be identified. "
                      "The artifacts contain different content and context with no overlaps (no trace-link)"]
RANKING_RANGE = range(RANKING_MAX_SCORE, RANKING_MIN_SCORE - 1,
                      -round(((RANKING_MAX_SCORE - RANKING_MIN_SCORE) / len(RANKING_CATEGORIES))))
SCORE_INSTRUCTIONS = SelectQuestionPrompt(
    categories_are_continuous=True,
    categories=RANKING_CATEGORIES,
    numeric_category_range=RANKING_RANGE,
    instructions=f"IMPORTANTLY, use your previous answers to determine "
                 f"a score from anywhere from {RANKING_MIN_SCORE} to {RANKING_MAX_SCORE} "
                 f"representing the strength of the trace link between "
                 "the parent and child. The following can help guide your decision. "
                 f"Often, the relationship might fall somewhere between two categories. "
                 f"Since the score is continuous, you may select a score in between the categories to reflect this (e.g. 2.8). "
                 f"Rather than give a score of exactly {list(RANKING_RANGE)[floor(len(RANKING_CATEGORIES) / 2)]} "
                 f"indicating you are unsure, provide a score slightly above or below (e.g. 2.8) "
                 f"to indicate whether it is more likely a trace-link does (> 3) or does not exist (< 2). "
                 f"Note, generally if a relationship is truly unclear, no trace-link exists. ",
    response_tag=RANKING_SCORE_TAG,
    response_format="Enclose the score in {}",
    value_formatter=lambda tag, val: PromptUtil.strip_new_lines_and_extra_space(StrUtil.remove_substrings(val, [L_CARROT, R_CARROT])),
    default_factory=lambda tag, val: DEFAULT_SCORE)

QUESTION2 = QuestionnairePrompt(instructions="Below is a set of reasoning steps used to determine "
                                             "if each artifact is a child of the parent artifact. "
                                             "Starting with artifact ID 0, "
                                             "answer the following questions for each artifact. "
                                             f"Each set of answers for a single artifact should be enclosed in "
                                             f"inside of {PromptUtil.create_xml(RANKING_ARTIFACT_TAG)}",
                                response_manager=XMLResponseManager(response_tag=RANKING_ARTIFACT_TAG,
                                                                    response_instructions_format="Enclose the set of answers "
                                                                                                 "for EACH artifact inside of {}"),
                                use_multi_step_task_instructions=True,
                                question_prompts=[QuestionPrompt("Provide the ID of the artifact being processed ",
                                                                 response_manager=XMLResponseManager(response_tag=RANKING_ID_TAG,
                                                                                                     expected_response_type=int)),
                                                  QuestionnairePrompt(instructions=f"Within "
                                                                                   f"{PromptUtil.create_xml(RANKING_EXPLANATION_TAG)} "
                                                                                   f"provide three complete sentences "
                                                                                   f"answering the questions in the order below:",
                                                                      question_prompts=[
                                                                          QuestionPrompt(
                                                                              "What is this functionality of the child artifact? "
                                                                              "What module is the child a part of? "
                                                                              "Use the {PROJECT_SUMMARY_HEADER} "
                                                                              "to understand the system modules."),
                                                                          QuestionPrompt("How does the child's functionality "
                                                                                         "help the module it is a part of?"),
                                                                          QuestionPrompt("How does the child artifact functionality "
                                                                                         "affect the primary goal "
                                                                                         "of the parent artifact?")],
                                                                      enumeration_chars=["i", "ii", "iii", "iv", "v"],
                                                                      response_manager=XMLResponseManager(
                                                                          response_tag=RANKING_EXPLANATION_TAG)),
                                                  SCORE_INSTRUCTIONS,
                                                  Prompt(f"Make sure to enclose each set of answers "
                                                         f"for EACH individual artifact inside of {RANKING_ARTIFACT_TAG}")
                                                  ])
REWRITE_ARTIFACT_PROMPT = Prompt(f"Re-write the artifact below to highlight only key entities and actions and "
                                 f"removing any type-specific format. "
                                 f"For example, 'The system shall provide a secure login and authentication mechanism "
                                 f"for users to access their accounts.' could be re-writen to "
                                 f"'Secure login and authentication for user accounts'")
