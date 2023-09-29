from tgen.common.constants.tracing.ranking_constants import DEFAULT_ARTIFACT_HEADER, PROJECT_SUMMARY_HEADER, RANKING_ARTIFACT_TAG, \
    RANKING_ID_TAG, RANKING_MAX_SCORE, RANKING_PARENT_SUMMARY_TAG, \
    RANKING_SCORE_TAG, RANKING_MIN_SCORE
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.prompt import Prompt

from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.select_question_prompt import SelectQuestionPrompt

DEFAULT_RANKING_GOAL = Prompt(
    f"\n{PromptUtil.as_markdown_header('Goal')}\n"
    "You are an expert on the software project below. "
    f"This software project is described under `{PromptUtil.as_markdown_header(PROJECT_SUMMARY_HEADER)}`. "
    f"You are tasked with performing software traceability for a parent artifact "
    f"(enclosed in {PromptUtil.create_xml(RANKING_ARTIFACT_TAG)}) "
    f"against a list of candidate children artifacts under `{PromptUtil.as_markdown_header(DEFAULT_ARTIFACT_HEADER)}`. "
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
                      ], response_manager=PromptResponseManager(response_tag=RANKING_PARENT_SUMMARY_TAG))
RANKING_CATEGORIES = ["Artifacts have an direct 1:1 mapping based on closely-tied functionality "
                      "or a direct design or inheritance relationship",
                      "Artifacts have a clear primary-secondary relationship where one supports key functions of the other",
                      "Artifacts have some functional overlap, but neither is primarily supporting or dependent on the other",
                      "Artifacts have indirect relationships through secondary functions or peripheral impacts on each other",
                      "Artifacts have minimal overlap or impact on each other",
                      "No discernible relationship between artifacts can be identified"]


def default_score(_, __):
    return RANKING_MIN_SCORE


SCORE_INSTRUCTIONS = SelectQuestionPrompt(
    categories=RANKING_CATEGORIES,
    numeric_category_range=range(RANKING_MAX_SCORE, RANKING_MIN_SCORE - 1,
                                 -round((RANKING_MAX_SCORE - RANKING_MIN_SCORE) / len(RANKING_CATEGORIES))),
    instructions=f"Finally and IMPORTANTLY, user your previous answers to determine "
                 f"a score from {RANKING_MAX_SCORE}-{RANKING_MIN_SCORE} "
                 f"representing the strength of the trace link between "
                 "the parent and child. Using the following as guidelines: ",
    response_tag=RANKING_SCORE_TAG,
    default_factory=default_score)

QUESTION2 = QuestionnairePrompt(instructions="Below is a set of reasoning steps used to determine "
                                             "if each artifact is a child of the parent artifact. "
                                             "Starting with artifact ID 0, "
                                             "answer the following questions for each artifact. "
                                             f"Enclose ALL of the answers for EACH child artifact "
                                             f"inside of {PromptUtil.create_xml(RANKING_ARTIFACT_TAG)}",
                                response_manager=PromptResponseManager(response_tag=RANKING_ARTIFACT_TAG,
                                                                       response_instructions_format="Enclose ALL of your answers "
                                                                                                    "for each artifact inside of {}"),
                                use_multi_step_task_instructions=True,
                                question_prompts=[QuestionPrompt("Provide the ID of the artifact being processed ",
                                                                 PromptResponseManager(response_tag=RANKING_ID_TAG,
                                                                                       expected_response_type=int)),
                                                  QuestionPrompt("What components do each of the artifacts belong to? "
                                                                 "Do the components have directly related "
                                                                 "or supporting functionality? ",
                                                                 PromptResponseManager(response_tag="components")),
                                                  QuestionPrompt("What are the primary functions or purposes "
                                                                 "of each artifact? Are they closely aligned "
                                                                 "or more distantly related?",
                                                                 PromptResponseManager(response_tag="functionality")),
                                                  QuestionPrompt("Do the artifacts perform any unrelated functionalities or "
                                                                 "rely on different components/features "
                                                                 "that might weaken the trace?",
                                                                 PromptResponseManager(response_tag="weaken")),
                                                  QuestionPrompt("Do the artifacts rely on common inputs, "
                                                                 "produce common outputs, or share common data flows? ",
                                                                 PromptResponseManager(response_tag="data-flow")),
                                                  QuestionPrompt("Do the names or descriptions of the artifacts contain "
                                                                 "overlapping terms or concepts? ",
                                                                 PromptResponseManager(response_tag="terms")),
                                                  SCORE_INSTRUCTIONS,
                                                  QuestionPrompt("Write a brief explanation of why this score reflects the "
                                                                 "relationship between the two artifacts",
                                                                 PromptResponseManager(response_tag="justification"))
                                                  ])
