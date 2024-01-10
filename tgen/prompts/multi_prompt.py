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


class MultiPrompt(Prompt):
    """
    Contains a list of questions for the model to answer
    """

    def __init__(self, child_prompts: Union[List[Prompt], Dict[int, Prompt]], main_prompt_value: str = EMPTY_STRING, **prompt_vars):
        """
        Selects a prompt based on some condition.
        :param child_prompts: List of all candidate prompts that can be used.
        :param prompt_selector: The prompt will selected based on the conditional value.
        :param main_prompt_value: The value of the main prompt.
        :param prompt_vars: Any additional params for the prompt class.
        """
        if isinstance(child_prompts, Dict):
            starting_number = min(child_prompts.keys())
            child_prompts = [child_prompts[i] for i in range(starting_number, len(child_prompts) + starting_number)]
        self.child_prompts = [deepcopy(prompt) for prompt in child_prompts]
        super().__init__(main_prompt_value, **prompt_vars)

    def get_response_tags_for_prompt(self, prompt_index: int) -> Union[str, List[str]]:
        """
        Gets the response tags for a given prompt number
        :param prompt_index: The index of the question
        :return: The response tag ids
        """
        tag_ids = self.child_prompts[prompt_index].response_manager.get_all_tag_ids()
        if len(tag_ids) == 1:
            return tag_ids[0]
        return tag_ids

    def get_prompt_by_primary_tag(self, tag_id: str) -> Prompt:
        """
        Finds a prompt by its primary response tag
        :param tag_id: The id of the prompt's primary response tag
        :return: The prompt if it exists, else None
        """
        for prompt in self.child_prompts:
            tag_ids = prompt.get_all_response_tags()
            if len(tag_ids) > 0 and tag_ids[0] == tag_id:
                return prompt

    def get_all_response_tags(self) -> List[str]:
        """
        Gets the response tags for all questions
        :return: All response tag ids
        """
        all_tags = []
        for i in range(len(self.child_prompts)):
            tag_ids = self.child_prompts[i].response_manager.get_all_tag_ids()
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
        for prompt in self.child_prompts:
            prompt.format_value(**kwargs)
        return super().format_value(*args, **kwargs)

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the response from the model in the expected format for the prompt
        :param response: The model response
        :return: The formatted response
        """
        self.response_manager = self._update_response_manager_for_questions(self.response_manager)
        parsed = self.response_manager.parse_response(response)
        if isinstance(self.response_manager.response_tag, dict):
            start = 0
            parent_tag = self.response_manager.get_all_tag_ids()[0]
            parsed_items = []
            for item in parsed[parent_tag]:
                start = response.find(PromptUtil.create_xml_opening(parent_tag), start)
                end = response.find(PromptUtil.create_xml_closing(parent_tag), start)
                questions_parsed = self._parse_for_each_prompt(response[start:end])
                parsed_item = {k: v if k not in questions_parsed else questions_parsed[k] for k, v in item.items()}
                parsed_items.append(parsed_item)
                start = end
            parsed[parent_tag] = parsed_items
        else:
            parsed_children = self._parse_for_each_prompt(response)
            parsed.update(parsed_children)

        return parsed

    def _parse_for_each_prompt(self, response: str) -> Dict:
        """
        Parses the response for each of the question prompts
        :param response: The response
        :return: A dictionary containing all the parsed responses
        """
        parsed = {}
        for prompt in self.child_prompts:
            parsed_res = prompt.response_manager.parse_response(response)
            parsed.update(parsed_res)
        return parsed

    def __repr__(self) -> str:
        """
        Creates a representation of the questionnaire as a string
        :return: The quiestionnaire as a string
        """
        return f"{[repr(prompt) for prompt in self.child_prompts]}"
