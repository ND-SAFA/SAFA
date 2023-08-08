from tgen.common.util.prompt_util import PromptUtil
from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager, REQUIRE_ALL_TAGS
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.select_question_prompt import SelectQuestionPrompt

FORMAT_DIVIDER = NEW_LINE + "{}" + NEW_LINE

CHANGED_FILE_PROMPT = Prompt(f"{NEW_LINE}"
                             f"{PromptUtil.format_as_markdown('ORIGINAL CODE FILE:')}"
                             f"{FORMAT_DIVIDER}"
                             f"{PromptUtil.format_as_markdown('DIFF FOR CODE:')}"
                             f"{FORMAT_DIVIDER}")
DIFF_SUMMARY_TASKS = {
    1: QuestionPrompt("First, identify if imports or dependencies were changed. "
                      "If so, provide a brief summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="dependencies")),
    2: QuestionPrompt("Next, identify if any variables, methods or class names were renamed. "
                      "If so, provide a brief summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="renamed-vars")),
    3: QuestionPrompt("Next, determine if the code was refactored such that the changes did not change the original functionality. "
                      "If so, provide a brief summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="refactored")),
    4: QuestionPrompt("Then, identify if any new functionality has been added to the code. "
                      "If so, provide a brief summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="new-func")),
    5: QuestionPrompt("Next, identify if any pre-existing functionality has been modified in the code. "
                      "Do not consider new dependencies or imports in this task. "
                      "If so, provide a brief summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="modified-func")),
    6: QuestionPrompt("Then, identify if any bugs were fixed as a result of the code change. "
                      "If so, provide a brief summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="bug-fixes")),
    7: QuestionPrompt("Now, using all your responses, summarize the changes that were made to the code. ",
                      PromptResponseManager(response_tag="summary", required_tag_ids=REQUIRE_ALL_TAGS)),
    8: QuestionPrompt("Finally, summarize how this might impact the system as a whole. "
                      "Focus on the aspects that you can be certain of from the information provided. ",
                      PromptResponseManager(response_tag="impact", required_tag_ids=REQUIRE_ALL_TAGS)),
}
PROJECT_SUMMARY_PROMPT = Prompt(f"You are an expert on a software project and a change has recently been made to the project. "
                                f"Below is a software specification for the project, the original version of the code file, "
                                f"and its diff."
                                f"{NEW_LINE}" + "{summary}")
DIFF_SUMMARY_QUESTIONNAIRE = QuestionnairePrompt(
    question_prompts=DIFF_SUMMARY_TASKS,
    instructions=f"{PromptUtil.format_as_markdown('TASKS:')}{NEW_LINE}"
                 f"Complete the following tasks based on your understanding of the change to this project. "
                 f"When answering questions related to the diff, ONLY reference lines that begin with a + or -. "
                 f"Lines that begin with a + mean they were added and lines that begin with a - mean they were deleted."
                 f"All other lines are un-changeed. ")
