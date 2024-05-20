from tgen.common.constants.deliminator_constants import COMMA, EMPTY_STRING, NEW_LINE
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.prompt import Prompt
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.response_managers.abstract_response_manager import USE_ALL_TAGS
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager

DIFF_SUMMARY_TASKS = {
    0: QuestionPrompt("NOTE: For all analysis steps below, ONLY consider lines in the diff that begin with + or -. "
                      "Lines starting with + were added and lines starting with - were removed. "
                      "Ignore all other unchanged lines except as general context."),
    1: QuestionPrompt("First, check if any imports or dependencies were added or removed "
                      "based only on lines added (+) and removed (-) and summarize it if so. "
                      "Otherwise respond with 'no changes with dependencies or imports'.",
                      response_manager=XMLResponseManager(response_tag="dependencies-imports")),
    2: QuestionPrompt("Next, check if any variables, methods or class names were renamed "
                      "based only on lines added (+) and removed (-) and summarize it if so. "
                      "Otherwise respond with 'no renaming'.",
                      response_manager=XMLResponseManager(response_tag="renamed-vars")),
    3: QuestionPrompt("Check if the code was restructured or reordered but the overall functionality remained the same"
                      "based only on lines added (+) and removed (-) and summarize it if so. "
                      "Otherwise respond with 'no refactors'",
                      response_manager=XMLResponseManager(response_tag="refactored")),
    4: QuestionPrompt("Check if any new functionality or feature was added based only on lines added (+) and removed (-) "
                      "and summarize it if so. "
                      "Otherwise respond with 'no new functionality'.",
                      response_manager=XMLResponseManager(response_tag="new-func")),
    5: QuestionPrompt("Check if any existing functionality or feature was modified based only on lines added (+) and removed (-)"
                      "and summarize it if so. "
                      "Otherwise respond with 'no modified functionality'",
                      response_manager=XMLResponseManager(response_tag="modified-func")),
    6: QuestionPrompt("Check if any functionality or feature was removed based only on lines added (+) and removed (-) "
                      "and summarize it if so. "
                      "Otherwise respond with 'no removed functionality'",
                      response_manager=XMLResponseManager(response_tag="removed-func")),
    7: QuestionPrompt("Check if any bugs were fixed based only on lines added (+) and removed (-) "
                      "and summarize the fixes if so. "
                      "Otherwise respond with 'no bug fixes'.",
                      response_manager=XMLResponseManager(response_tag="bug-fixes")),
    8: QuestionPrompt("Now, using all your responses, summarize the changes that were made to the code. ",
                      response_manager=XMLResponseManager(response_tag="summary", required_tag_ids=USE_ALL_TAGS)),
    9: QuestionPrompt("Summarize how the changes may impact the system "
                      "Avoid speculation - "
                      "only include potential impacts that can be reasonably inferred from the information provided.",
                      response_manager=XMLResponseManager(response_tag="impact", required_tag_ids=USE_ALL_TAGS)),
}
ADDED_PROMPT = QuestionPrompt("Identify what new functionality was added in this code file",
                              response_manager=XMLResponseManager(response_tag="new-func"))
DELETED_PROMPT = QuestionPrompt("Identify what existing functionality was removed in this code file",
                                response_manager=XMLResponseManager(response_tag="removed-func"))
DIFF_SUMMARY_STARTER_PROMPT = Prompt(f"You are an expert on a software project and a change has recently been made to the project. "
                                     f"Below is a software specification for the project, context/documentation surrounding the code, "
                                     f"the original version of the code file, "
                                     f"and its diff."
                                     f"{NEW_LINE}" + "{summary}"
                                                     f"{NEW_LINE}" + "{context}")
DIFF_SUMMARY_QUESTIONNAIRE = QuestionnairePrompt(
    question_prompts=DIFF_SUMMARY_TASKS,
    instructions=f"{PromptUtil.as_markdown_header('TASKS:')}{NEW_LINE}"
                 f"Complete the following tasks based on your understanding of the change to this project. ")

CHANGE_SUMMARY_STARTER_PROMPT = Prompt(
    f"You are an expert on a software project and a Pull Request has recently been created on the project. "
    f"Below is a software specification for the project and a description of each change that was made as a part of the PR."
    f"{NEW_LINE}" + "{summary}")

CHANGE_SUMMARY_TASKS = {
    1: QuestionPrompt("First, group together changes that are aimed at the same, meaningful system-level change. "
                      "Importantly, each group should represent only ONE meaningful system-level change and ONE change type. "
                      "Additionally, all major changes should be captured in at least one group. "
                      "For each group, provide a detailed meaningful description of the change as well as the affected files, "
                      "and ONE change type that BEST describes the change. "
                      "Change types: {categories}.",
                      response_manager=XMLResponseManager(
                          value_formatter=lambda tag, val: [v.replace(NEW_LINE, EMPTY_STRING).strip() for v in val.split(COMMA)]
                          if tag == "filenames" or tag == "type" else val,
                          required_tag_ids=USE_ALL_TAGS,
                          response_tag={"group": ["filenames", "change", "type"]},
                          response_instructions_format="Each group should be enclosed in {} "
                                                       "with the names of the related files in a comma-deliminated list inside of {}, "
                                                       "a specific, detailed description of the change in {}, "
                                                       "and select exactly ONE (1) change type that BEST describes the group "
                                                       "(do not select multiple) and enclose the SINGLE change type in {}. ")),
    2: QuestionPrompt("Then, create a summary that gives an overview of all changes and the key highlights. "
                      "The goal of the summary is to consolidate all of the change analysis into a high-level overview that "
                      "captures the most important updates and focuses on communicating the key takeaways. ",
                      response_manager=XMLResponseManager(response_tag="low-level-summary", required_tag_ids=USE_ALL_TAGS)),
    3: QuestionPrompt("Finally, summarize the changes "
                      "but in non-technical terms for someone unfamiliar with the codebase. "
                      "Focus on aspects that are most important from a user's perspective, "
                      "based only on the information provided about the system and changes. "
                      "Do not make assumptions or guesses about impact that is not clear from the given information. ",
                      response_manager=XMLResponseManager(response_tag="user-level-summary", required_tag_ids=USE_ALL_TAGS)),
}

CHANGE_SUMMARY_QUESTIONNAIRE = QuestionnairePrompt(
    question_prompts=CHANGE_SUMMARY_TASKS,
    instructions=f"{NEW_LINE}{PromptUtil.as_markdown_header(f'TASKS:')}{NEW_LINE}"
                 f"Complete the following tasks based on your understanding of the changes to this project. ")

IMPACTS_PROMPT = Prompt("TASK: Based on your understanding of the system, the changes, and their potential impacts, "
                        "summarize the potential effects of all changes on the system. "
                        "Consider how the updates may impact "
                        "performance, reliability, security, sustainability, and usability. "
                        "Focus on identifying plausible effects using the information provided, but avoid speculation. ",
                        response_manager=XMLResponseManager(response_tag="potential-impact", required_tag_ids=USE_ALL_TAGS)
                        )
