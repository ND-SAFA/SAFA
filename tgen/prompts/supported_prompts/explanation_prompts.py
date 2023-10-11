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
    "You are tasked with performing software traceability for a {target_type} (parent) "
    "and a candidate {source_type} artifact (child). "
)

EXPLANATION_TASK_QUESTIONNAIRE = QuestionnairePrompt(instructions="Two artifacts are considered to be traced if they have related "
                                                                  "functionality, depend on the same features/data, "
                                                                  "or directly impact each other through inputs, outputs or changes. "
                                                                  "IGNORE and do NOT mention scope or level of details "
                                                                  "in your responses since a higher-level {target_type} "
                                                                  "could be traced to a low-level level {source_type} "
                                                                  "To help you determine if the artifacts are traced, "
                                                                  "you must complete the reasoning steps below. "
                                                                  "More yeses to the questions indicate a stronger relationship "
                                                                  "while more nos indicate a weaker one. "
                                                                  "The strength of the relationship (likelihood of being linked) "
                                                                  "was originally scored to be {orig_score} on a scale from "
                                                                  f"{RANKING_MIN_SCORE}-{RANKING_MAX_SCORE} "
                                                                  "where a higher score represents a stronger relationship. "
                                                                  "Use this to guide your answers. " 
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
                                                                        "of each artifact. How might the functionality of one "
                                                                        "artifact impact the other?",
                                                                        PromptResponseManager(response_tag="functionality")),
                                                         QuestionPrompt("Do the artifacts rely on common inputs, "
                                                                        "produce common outputs, or share common data flows? ",
                                                                        PromptResponseManager(response_tag="data-flow")),
                                                         QuestionPrompt("Could one artifact be derived from, "
                                                                        "decomposed from, or an implementation of the other, meaning "
                                                                        "that is was created by extracting or breaking down the "
                                                                        "other artifact into a smaller, more detailed components? ",
                                                                        PromptResponseManager(response_tag="decomposition")),
                                                         QuestionPrompt("If one artifact changed, "
                                                                        "would it impact or necessitate changes in the other "
                                                                        "at the level of implementation?",
                                                                        PromptResponseManager(response_tag="impact")),
                                                         SCORE_INSTRUCTIONS,
                                                         QuestionPrompt("Using your previous responses and both scores given, "
                                                                        "write a brief explanation that accesses the strength of the "
                                                                        "relationship between the two artifacts and why you "
                                                                        "believe they are mostly likely traced or un-traced. "
                                                                        "Do NOT mention differences in abstraction level "
                                                                        "or scope in your justification. "
                                                                        "Importantly, do NOT reference the specific score "
                                                                        "in the justification. ",
                                                                        PromptResponseManager(
                                                                            response_tag=JUSTIFICATION_TAG))
                                                     ])
