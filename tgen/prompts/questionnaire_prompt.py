from copy import deepcopy
from string import ascii_uppercase
from typing import Any, Dict, List, Union

from tgen.common.constants.deliminator_constants import COMMA, EMPTY_STRING, NEW_LINE, SPACE
from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.override import overrides
from tgen.common.util.prompt_util import PromptUtil
from tgen.common.util.str_util import StrUtil
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager

TASK_HEADER = 'TASKS:'


class QuestionnairePrompt(Prompt):
    """
    Contains a list of questions for the model to answer
    """

    def __init__(self, question_prompts: Union[List[Prompt], Dict[int, Prompt]], instructions: str = EMPTY_STRING,
                 response_manager: PromptResponseManager = None, enumeration_chars: List[str] = ascii_uppercase,
                 use_multi_step_task_instructions: bool = False, prompt_id: str = None):
        """
        Initializes the questionnaire with the instructions and the questions that will make up the prompt
        :param question_prompts: The list of question prompts to include in the questionnaire
        :param instructions: Any instructions necessary with the questionnaire
        :param response_manager: Manages the responses from the prompt
        :param enumeration_chars: The list of characters to use to enumerate the questions (must include one for each question)
        :param use_multi_step_task_instructions: If True, uses default instructions for task involving multiple steps
        """
        if isinstance(question_prompts, Dict):
            starting_number = min(question_prompts.keys())
            question_prompts = [question_prompts[i] for i in range(starting_number, len(question_prompts) + starting_number)]
        self.question_prompts = [deepcopy(prompt) for prompt in question_prompts]
        self.enumeration_chars = enumeration_chars
        self.use_bullets_for_enumeration = len(self.enumeration_chars) == 1
        if self.use_bullets_for_enumeration:
            self.enumeration_chars = [self.enumeration_chars[0] for _ in self.question_prompts]
        self.use_multi_step_task_instructions = use_multi_step_task_instructions
        if response_manager and not isinstance(response_manager.response_tag, dict):
            all_tags = self.get_all_response_tags()
            if len(all_tags) > 0:
                params = DataclassUtil.convert_to_dict(PromptResponseManager, response_tag={response_manager.response_tag: all_tags})
                response_manager = PromptResponseManager(**params)

        super().__init__(instructions, response_manager=response_manager, prompt_id=prompt_id)

    def get_response_tags_for_question(self, question_index: int) -> Union[str, List[str]]:
        """
        Gets the response tags for a given question number
        :param question_index: The index of the question
        :return: The response tag ids
        """
        tag_ids = self.question_prompts[question_index].response_manager.get_all_tag_ids()
        if len(tag_ids) == 1:
            return tag_ids[0]
        return tag_ids

    def get_prompt_by_primary_tag(self, tag_id: str) -> Prompt:
        """
        Finds a prompt by its primary response tag
        :param tag_id: The id of the prompt's primary response tag
        :return: The prompt if it exists, else None
        """
        for prompt in self.question_prompts:
            tag_ids = prompt.get_all_response_tags()
            if len(tag_ids) > 0 and tag_ids[0] == tag_id:
                return prompt

    def get_all_response_tags(self) -> List[str]:
        """
        Gets the response tags for all questions
        :return: All response tag ids
        """
        all_tags = []
        for i in range(len(self.question_prompts)):
            tag_ids = self.question_prompts[i].response_manager.get_all_tag_ids()
            if isinstance(tag_ids, list):
                all_tags.extend(tag_ids)
            else:
                all_tags.append(tag_ids)
        return all_tags

    @overrides(Prompt)
    def format_value(self, *args: object, **kwargs: object) -> str:
        """
        Formats the value of all question prompts
        :param args: Args for formatting
        :param kwargs: Kwargs for formatting
        :return: None
        """
        for prompt in self.question_prompts:
            prompt.format_value(**kwargs)
        return super().format_value(*args, **kwargs)

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the response from the model in the expected format for the prompt
        :param response: The model response
        :return: The formatted response
        """
        parsed = self.response_manager.parse_response(response)
        if isinstance(self.response_manager.response_tag, dict):
            start = 0
            parent_tag = self.response_manager.get_all_tag_ids()[0]
            parsed_items = []
            for item in parsed[parent_tag]:
                start = response.find(PromptUtil.create_xml_opening(parent_tag), start)
                end = response.find(PromptUtil.create_xml_closing(parent_tag), start)
                questions_parsed = self._parse_for_each_question(response[start:end])
                parsed_item = {k: v if k not in questions_parsed else questions_parsed[k] for k, v in item.items()}
                parsed_items.append(parsed_item)
                start = end
            parsed[parent_tag] = parsed_items
        else:
            parsed = self._parse_for_each_question(response)

        return parsed

    def _parse_for_each_question(self, response: str) -> Dict:
        """
        Parses the response for each of the question prompts
        :param response: The response
        :return: A dictionary containing all the parsed responses
        """
        parsed = {}
        for prompt in self.question_prompts:
            parsed_res = prompt.response_manager.parse_response(response)
            parsed.update(parsed_res)
        return parsed

    @overrides(Prompt)
    def _build(self, child: bool = False, **kwargs) -> str:
        """
        Constructs the prompt in the following format:
        [Instructions]
        A) Question 1
        B) ...
        C) Question n
        :param child: If True, adds additional indents
        :return: The formatted prompt
        """
        if self.use_multi_step_task_instructions and TASK_HEADER not in self.value:
            self.value = self._create_multi_step_task_instructions(self.enumeration_chars, self.question_prompts, self.value)
        update_value = DictUtil.get_kwarg_values(kwargs=kwargs, update_value=False, pop=True)
        if update_value:
            self.format_value(**kwargs)
        question_format = "{}) {}" if not self.use_bullets_for_enumeration else "{} {}"
        if child:
            question_format = PromptUtil.indent_for_markdown(question_format)
        formatted_questions = NEW_LINE.join([question_format.format(self.enumeration_chars[i % len(self.enumeration_chars)],
                                                                    question.build(child=True, **kwargs))
                                             for i, question in enumerate(self.question_prompts)])
        instructions = f"{self.value}{NEW_LINE}" if self.value else EMPTY_STRING
        final = f"{instructions}{formatted_questions}{NEW_LINE}"
        if not update_value:
            final = StrUtil.format_selective(final, **kwargs)
        return final

    @staticmethod
    def _create_multi_step_task_instructions(enumeration_chars: List[str], question_prompts: List[Prompt],
                                             special_instructions: str = None) -> str:
        """
        Creates the default instructions for a multi-step task
        :param enumeration_chars: The enumeration chars being used
        :param question_prompts: The prompts making up the questionnaire
        :return: The instructions for a multi-step task
        """
        n_questions = len(question_prompts)
        enumerations_for_task = f'{COMMA}{SPACE}'.join(enumeration_chars[:n_questions - 1])
        base_instructions = f"Below are {len(question_prompts)} steps to complete. " \
                            f"Ensure that you answer {enumerations_for_task} and {enumeration_chars[n_questions - 1]}"
        instructions = [PromptUtil.as_markdown_header(TASK_HEADER), PromptUtil.as_markdown_italics(base_instructions)]
        if special_instructions:
            instructions.append(special_instructions)
        return f'{NEW_LINE}{NEW_LINE.join(instructions)}{NEW_LINE}'

    def set_instructions(self, instructions: str) -> None:
        """
        Sets the string as the instructions for the questionnaire.
        :param instructions: The prefix to the questions.
        :return: None
        """
        self.value = instructions

    def __repr__(self) -> str:
        """
        Creates a representation of the questionnaire as a string
        :return: The quiestionnaire as a string
        """
        return f"{[repr(prompt) for prompt in self.question_prompts]}"
