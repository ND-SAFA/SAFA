from tgen.common.constants.tracing.ranking_constants import PROJECT_SUMMARY_HEADER, RANKING_ARTIFACT_TAG, \
    RANKING_ID_TAG, RANKING_MAX_SCORE, RANKING_PARENT_SUMMARY_TAG, \
    RANKING_SCORE_TAG, RANKING_MIN_SCORE, ARTIFACT_HEADER, JUSTIFICATION_TAG
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.prompt import Prompt

from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.select_question_prompt import SelectQuestionPrompt
from tgen.prompts.supported_prompts.tracing_prompts import SCORE_INSTRUCTIONS

EXPLANATION_GOAL = Prompt(
    f"\n{PromptUtil.as_markdown_header('Goal')}\n"
    "You are an expert on the software project below. "
    f"This software project is described under `{PromptUtil.as_markdown_header(PROJECT_SUMMARY_HEADER)}`. "
    f"You are tasked with performing software traceability for a parent artifact "
    f"and a candidate children artifact`. "
)

EXPLANATION_TASK_QUESTIONNAIRE = QuestionnairePrompt(instructions="In order to determine if the artifacts are traced, "
                                                                  "you must complete the reasoning steps below. "
                                                                  "The steps will help you determine if the child and parent "
                                                                  "are actually related or whether there is no link between them."
                                                                  "Importantly, provide all answers as complete sentences "
                                                                  "that would be able to "
                                                                  "be understood without seeing the question. "
                                                                  "Be as a specific as possible.",
                                                     use_multi_step_task_instructions=True,
                                                     question_prompts=[
                                                         QuestionPrompt("What sub-systems do each of the artifacts belong to? ",
                                                                        PromptResponseManager(response_tag="sub-systems")),
                                                         QuestionPrompt("What entities of the system "
                                                                        "do each of the artifacts interact with? ",
                                                                        PromptResponseManager(response_tag="entities")),
                                                         QuestionPrompt("Which of the features would each artifact depend on? ",
                                                                        PromptResponseManager(response_tag="features")),
                                                         QuestionPrompt("What are the primary functions or purposes "
                                                                        "of each artifact? Are they closely aligned "
                                                                        "or more distantly related?",
                                                                        PromptResponseManager(response_tag="functionality")),
                                                         QuestionPrompt("Do the artifacts rely on common inputs, "
                                                                        "produce common outputs, or share common data flows? ",
                                                                        PromptResponseManager(response_tag="data-flow")),
                                                         QuestionPrompt("What differences between the artifacts may indicate "
                                                                        "the artifacts are not traced?",
                                                                        PromptResponseManager(response_tag="un-related")),
                                                         SCORE_INSTRUCTIONS,
                                                         QuestionPrompt("Include a brief explanation of why this score "
                                                                        "reflects the relationship between the two artifacts. "
                                                                        "Importantly, the scores will later be scaled so "
                                                                        "do NOT reference the specific score "
                                                                        "in the justification. ",
                                                                        PromptResponseManager(
                                                                            response_tag=JUSTIFICATION_TAG))
                                                     ])
