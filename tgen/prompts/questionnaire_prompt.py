from string import ascii_uppercase
from typing import Dict, List, Union

from tgen.common.constants.deliminator_constants import COMMA, EMPTY_STRING, NEW_LINE, SPACE
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.override import overrides
from tgen.common.util.prompt_util import PromptUtil
from tgen.common.util.str_util import StrUtil
from tgen.prompts.multi_prompt import MultiPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.response_managers.abstract_response_manager import AbstractResponseManager

TASK_HEADER = 'TASKS:'


class QuestionnairePrompt(MultiPrompt):
    """
    Contains a list of questions for the model to answer
    """

    def __init__(self, question_prompts: Union[List[Prompt], Dict[int, Prompt]], instructions: str = EMPTY_STRING,
                 response_manager: AbstractResponseManager = None, enumeration_chars: List[str] = ascii_uppercase,
                 use_multi_step_task_instructions: bool = False, prompt_args: PromptArgs = None):
        """
        Initializes the questionnaire with the instructions and the questions that will make up the prompt
        :param question_prompts: The list of question prompts to include in the questionnaire
        :param instructions: Any instructions necessary with the questionnaire
        :param response_manager: Manages the responses from the prompt
        :param enumeration_chars: The list of characters to use to enumerate the questions (must include one for each question)
        :param use_multi_step_task_instructions: If True, uses default instructions for task involving multiple steps
        :param prompt_args: The args to the base prompt.
        """
        self.enumeration_chars = enumeration_chars
        self.use_bullets_for_enumeration = len(self.enumeration_chars) == 1
        self.use_multi_step_task_instructions = use_multi_step_task_instructions
        super().__init__(main_prompt_value=instructions, child_prompts=question_prompts,
                         response_manager=response_manager, prompt_args=prompt_args)

    def set_instructions(self, instructions: str) -> None:
        """
        Sets the string as the instructions for the questionnaire.
        :param instructions: The prefix to the questions.
        :return: None
        """
        self.value = instructions

    @overrides(Prompt)
    def _build(self, child_num: int = 0, **kwargs) -> str:
        """
        Constructs the prompt in the following format:
        [Instructions]
        A) Question 1
        B) ...
        C) Question n
        :param child_num: Corresponds to the number of idents for nested questionnaires.
        :return: The formatted prompt
        """
        if self.use_bullets_for_enumeration:
            self.enumeration_chars = [self.enumeration_chars[0] for _ in self.child_prompts]
        if self.use_multi_step_task_instructions and TASK_HEADER not in self.value:
            self.value = self._create_multi_step_task_instructions()
        update_value = DictUtil.get_kwarg_values(kwargs=kwargs, update_value=False, pop=True)
        if update_value:
            self.format_value(**kwargs)
        question_format = "{}) {}" if not self.use_bullets_for_enumeration else "{} {}"
        if child_num > 0:
            question_format = PromptUtil.indent_for_markdown(question_format, level=child_num)
        formatted_questions = NEW_LINE.join([question_format.format(self.enumeration_chars[i % len(self.enumeration_chars)],
                                                                    question.build(child_num=child_num + 1, **kwargs))
                                             for i, question in enumerate(self.child_prompts)])
        instructions = f"{self.value}{NEW_LINE}" if self.value else EMPTY_STRING
        final = f"{instructions}{formatted_questions}{NEW_LINE}"
        if not update_value:
            final = StrUtil.format_selective(final, **kwargs)
        return final

    def _create_multi_step_task_instructions(self) -> str:
        """
        Creates the default instructions for a multi-step task
        :return: The instructions for a multi-step task
        """
        n_questions = len(self.child_prompts)
        enumerations_for_task = f'{COMMA}{SPACE}'.join(self.enumeration_chars[:n_questions - 1])
        base_instructions = f"Below are {len(self.child_prompts)} steps to complete."
        if not self.use_bullets_for_enumeration and len(self.child_prompts) > 1:
            base_instructions += f" Ensure that you answer {enumerations_for_task} and {self.enumeration_chars[n_questions - 1]}"
        instructions = [PromptUtil.as_markdown_header(TASK_HEADER), PromptUtil.as_markdown_italics(base_instructions)]
        if self.value:
            instructions.append(self.value)
        return f'{NEW_LINE}{NEW_LINE.join(instructions)}{NEW_LINE}'
