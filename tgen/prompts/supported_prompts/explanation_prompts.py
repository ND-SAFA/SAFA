from tgen.common.constants.ranking_constants import PROJECT_SUMMARY_HEADER, RANKING_MAX_SCORE, RANKING_MIN_SCORE, JUSTIFICATION_TAG
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.prompt import Prompt

from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
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
                                                                  "are actually related or whether there is no link between them. "
                                                                  "More yeses to the questions indicate a stronger relationship "
                                                                  "while more nos indicate a weaker one. "
                                                                  "The strength of the relationship was originally scored to be "
                                                                  "{orig_score} on a scale from "
                                                                  f"{RANKING_MIN_SCORE}-{RANKING_MAX_SCORE} "
                                                                  "where a higher score represents a stronger relationship. "
                                                                  "Use this to guide your answers."                                             
                                                                  "Importantly, provide all answers as complete sentences "
                                                                  "that would be able to "
                                                                  "be understood without seeing the question. "
                                                                  "Be as a specific as possible.",
                                                     use_multi_step_task_instructions=True,
                                                     question_prompts=[
                                                         QuestionPrompt("Do the artifacts belong to the same sub-system or "
                                                                        "depend on the same entities or features?  ",
                                                                        PromptResponseManager(response_tag="dependencies")),
                                                         QuestionPrompt("What are the primary functions or purposes "
                                                                        "of each artifact and are they closely aligned?",
                                                                        PromptResponseManager(response_tag="functionality")),
                                                         QuestionPrompt("Do the artifacts rely on common inputs, "
                                                                        "produce common outputs, or share common data flows? ",
                                                                        PromptResponseManager(response_tag="data-flow")),
                                                         QuestionPrompt("Could one artifact be derived from "
                                                                        "or decomposed from the other?",
                                                                        PromptResponseManager(response_tag="decomposition")),
                                                         QuestionPrompt("If one artifact changed, "
                                                                        "would it impact or necessitate changes in the other?",
                                                                        PromptResponseManager(response_tag="impact")),
                                                         QuestionPrompt("Are key terms, concepts, or components referenced "
                                                                        "in one artifact also present in the other? ",
                                                                        PromptResponseManager(response_tag="terms")),
                                                         SCORE_INSTRUCTIONS,
                                                         QuestionPrompt("Using your previous responses and the scores given, "
                                                                        "write a brief explanation that accesses the strength of the "
                                                                        "relationship between the two artifacts. "
                                                                        "Importantly, do NOT reference the specific score "
                                                                        "in the justification. ",
                                                                        PromptResponseManager(
                                                                            response_tag=JUSTIFICATION_TAG))
                                                     ])
