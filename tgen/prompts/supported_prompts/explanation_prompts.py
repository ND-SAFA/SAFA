from tgen.common.constants.ranking_constants import CHANGE_IMPACT_TAG, DERIVATION_TAG, ENTITIES_TAG, FUNCTIONALITY_TAG, \
    JUSTIFICATION_TAG, PROJECT_SUMMARY_HEADER, \
    RANKING_MAX_SCORE, \
    RANKING_MIN_SCORE, \
    SUB_SYSTEMS_TAG
from common_resources.tools.util.prompt_util import PromptUtil
from tgen.prompts.prompt import Prompt
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager
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
                                                         QuestionPrompt("What sub-systems and components do the artifacts belong to, "
                                                                        "impact or reference? Are any of the sub-systems/components "
                                                                        "shared between the two artifacts?",
                                                                        response_manager=XMLResponseManager(
                                                                            response_tag=SUB_SYSTEMS_TAG)),
                                                         QuestionPrompt("What inputs, outputs, entities or technical details "
                                                                        "are specified in each artifact? Do the artifacts "
                                                                        "reference any of the same ones?",
                                                                        response_manager=XMLResponseManager(
                                                                            response_tag=ENTITIES_TAG)),
                                                         QuestionPrompt("What are the primary functions or purposes "
                                                                        "of each artifact? Could the functionality of one "
                                                                        "artifact impact the other? Does one artifact reference "
                                                                        "functionality that is fulfilled in the other?",
                                                                        response_manager=XMLResponseManager(
                                                                            response_tag=FUNCTIONALITY_TAG)),
                                                         QuestionPrompt("Could one artifact be derived from, "
                                                                        "decomposed from, or be an implementation of the other? "
                                                                        "This means that it was created by extracting, "
                                                                        "breaking down, or implementing a portion of the "
                                                                        "other artifact, generally resulting in "
                                                                        "a smaller, more detailed component at a lower-level. ",
                                                                        response_manager=XMLResponseManager(
                                                                            response_tag=DERIVATION_TAG)),
                                                         QuestionPrompt("If one artifact changed, "
                                                                        "would it impact or necessitate changes in the other? "
                                                                        "Could a change in one create a misalignment with the "
                                                                        "capabilities/functionality described in the other?",
                                                                        response_manager=XMLResponseManager(
                                                                            response_tag=CHANGE_IMPACT_TAG)),
                                                         SCORE_INSTRUCTIONS,
                                                         QuestionPrompt("Using your previous responses and both scores given, "
                                                                        "write a brief explanation that accesses the strength of the "
                                                                        "relationship between the two artifacts and why you "
                                                                        "believe they are mostly likely traced or un-traced. "
                                                                        "Importantly, do NOT reference the specific score "
                                                                        "in the justification. ",
                                                                        response_manager=XMLResponseManager(
                                                                            response_tag=JUSTIFICATION_TAG))
                                                     ])
