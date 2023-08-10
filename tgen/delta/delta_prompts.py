from tgen.common.util.prompt_util import PromptUtil
from tgen.constants.deliminator_constants import NEW_LINE, COMMA
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager, REQUIRE_ALL_TAGS
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.select_question_prompt import SelectQuestionPrompt

FORMAT_DIVIDER = NEW_LINE + "{}" + NEW_LINE + NEW_LINE

CHANGED_FILE_PROMPT = Prompt(f"{FORMAT_DIVIDER}"
                             f"{PromptUtil.format_as_markdown_header('ORIGINAL CODE FILE:')}"
                             f"{FORMAT_DIVIDER}"
                             f"{PromptUtil.format_as_markdown_header('DIFF FOR CODE:')}"
                             f"{FORMAT_DIVIDER}")
DIFF_SUMMARY_TASKS = {
    1: QuestionPrompt("First, identify if imports or dependencies were changed. "
                      "If so, provide a detailed summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="dependencies-imports")),
    2: QuestionPrompt("Next, identify if any variables, methods or class names were renamed. "
                      "If so, provide a detailed summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="renamed-vars")),
    3: QuestionPrompt("Next, determine if the code was refactored such that the changes did not change the original functionality. "
                      "This might include re-ordering or re-structuring the code."
                      "If so, provide a detailed summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="refactored")),
    4: QuestionPrompt("Then, identify if any new functionality has been added to the code. "
                      "If so, provide a detailed summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="new-func")),
    5: QuestionPrompt("Next, identify if any pre-existing functionality has been modified in the code. "
                      "Do not consider new dependencies or imports in this task. "
                      "If so, provide a detailed summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="modified-func")),
    6: QuestionPrompt("Next, identify if any functionality has been removed from the code. "
                      "If so, provide a detailed summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="removed-func")),
    7: QuestionPrompt("Then, identify if any bugs were fixed as a result of the code change. "
                      "If so, provide a detailed summary. Otherwise response with no.",
                      PromptResponseManager(response_tag="bug-fixes")),
    8: QuestionPrompt("Now, using all your responses, summarize the changes that were made to the code. ",
                      PromptResponseManager(response_tag="summary", required_tag_ids=REQUIRE_ALL_TAGS)),
    9: QuestionPrompt("Finally, summarize how this might impact the system as a whole. "
                      "Focus on the aspects that you can be certain of from the information provided. ",
                      PromptResponseManager(response_tag="impact", required_tag_ids=REQUIRE_ALL_TAGS)),
}
DIFF_SUMMARY_STARTER_PROMPT = Prompt(f"You are an expert on a software project and a change has recently been made to the project. "
                                     f"Below is a software specification for the project, context/documentation surrounding the code, "
                                     f"the original version of the code file, "
                                     f"and its diff."
                                     f"{NEW_LINE}" + "{summary}"
                                                     f"{NEW_LINE}" + "{context}")
DIFF_SUMMARY_QUESTIONNAIRE = QuestionnairePrompt(
    question_prompts=DIFF_SUMMARY_TASKS,
    instructions=f"{PromptUtil.format_as_markdown_header('TASKS:')}{NEW_LINE}"
                 f"Complete the following tasks based on your understanding of the change to this project. "
                 f"When answering questions related to the diff, ONLY reference lines that begin with a + or -. "
                 f"Lines that begin with a + mean they were added and lines that begin with a - mean they were deleted."
                 f"All other lines are un-changed. ")

CHANGE_SUMMARY_STARTER_PROMPT = Prompt(
    f"You are an expert on a software project and a Pull Request has recently been created on the project. "
    f"Below is a software specification for the project and a description of each change that was made as a part of the PR."
    f"{NEW_LINE}" + "{summary}")

CHANGE_SUMMARY_TASKS = {
    1: QuestionPrompt("First, group changes the are related together. "
                      "For each change, include the files that the change affected, "
                      "and select the ONE category that BEST describes the change type: {categories}.",
                      PromptResponseManager(
                          formatter=lambda tag, val: val.split(COMMA) if tag == "filenames" else val,
                          response_tag={"group": ["filenames", "change", "type"]},
                          response_instructions_format="Each group should be enclosed in {} "
                                                       "with the names of the related files in a comma-deliminated list inside of {}, "
                                                       "a detailed description of the change in {}, "
                                                       "and the one type of change that best describes it in {}. ")),
    2: QuestionPrompt("Then, create a detailed summary that gives an overview of all changes and the key highlights. ",
                      PromptResponseManager(response_tag="low-level-summary")),
    3: QuestionPrompt("Finally, describe the changes to a high-level manager who is unfamiliar with the code. "
                      "Focus on changes that would affect the end-user. ",
                      PromptResponseManager(response_tag="high-level-summary")),
}

CHANGE_SUMMARY_QUESTIONNAIRE = QuestionnairePrompt(
    question_prompts=CHANGE_SUMMARY_TASKS,
    instructions=f"{NEW_LINE}{PromptUtil.format_as_markdown_header(f'TASKS:')}{NEW_LINE}"
                 f"Complete the following tasks based on your understanding of the changes to this project. ")
