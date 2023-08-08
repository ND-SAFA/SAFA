from tgen.common.util.prompt_util import PromptUtil
from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.select_question_prompt import SelectQuestionPrompt

FORMAT_DIVIDER = NEW_LINE + "{}" + NEW_LINE

CHANGED_FILE_PROMPT = Prompt(f"PromptUtil.format_as_markdown('ORIGINAL:') "
                             f"{FORMAT_DIVIDER} "
                             f"PromptUtil.format_as_markdown('DIFF:')"
                             f"{FORMAT_DIVIDER}")
DIFF_SUMMARY_TASKS = {1: QuestionPrompt("First, identify if any new functionality has been added to the code. "
                                        "If so, provide a brief summary. Otherwise skip this task.",
                                        PromptResponseManager(response_tag="new-func")),
                      2: QuestionPrompt("Next, identify if any pre-existing functionality has been modified in the code. "
                                        "If so, provide a brief summary. Otherwise skip this task.",
                                        PromptResponseManager(response_tag="modified-func")),
                      3: QuestionPrompt("Then, identify if any bugs were fixed as a result of the code change. "
                                        "If so, provide a brief summary. Otherwise skip this task.",
                                        PromptResponseManager(response_tag="bug-fixes")),
                      4: SelectQuestionPrompt(categories={"RENAME": "Variables, including method or class names, were renamed",
                                                          "IMPORTS": "Imports paths were modified",
                                                          "NEW-FUNCTIONALITY": "New functionality was added",
                                                          "MODIFIED-FUNCTIONALITY": "Existing functionality was modified",
                                                          "BUG-FIX": "A bug was fixed by the change",
                                                          "OTHER": "None of these categories apply"},
                                              instructions="Select all of the categories that apply to the change",
                                              response_format="Enclose the name of all "
                                                              "applicable categories in a comma-deliminated list inside of {}",
                                              response_tag="categories",
                                              multiple_responses_allowed=True),
                      5: QuestionPrompt("Finally, using all your responses, summarize all changes that were made to the code. "
                                        "Focus on how this change could affect the system as a whole. ",
                                        PromptResponseManager(response_tag="summary"))
                      }
PROJECT_SUMMARY_PROMPT = Prompt(f"You are an expert on a software project and a change has recently been made to the project. "
                                f"{PromptUtil.format_as_markdown('PROJECT SUMMARY:')}{NEW_LINE}" + "{summary}")
DIFF_SUMMARY_QUESTIONNAIRE = QuestionnairePrompt(
    question_prompts=DIFF_SUMMARY_TASKS,
    instructions="Complete the following tasks related to the change to this project. ")
