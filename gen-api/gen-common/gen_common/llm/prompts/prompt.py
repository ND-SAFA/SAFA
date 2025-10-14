from typing import Any, Dict, List

from gen_common.constants.symbol_constants import EMPTY_STRING, NEW_LINE, SPACE
from gen_common.llm.prompts.prompt_args import PromptArgs
from gen_common.llm.response_managers.abstract_response_manager import AbstractResponseManager
from gen_common.llm.response_managers.xml_response_manager import XMLResponseManager
from gen_common.util.dict_util import DictUtil
from gen_common.util.prompt_util import PromptUtil
from gen_common.util.str_util import StrUtil


class Prompt:
    """
    Represents a prompt with special formatting that allows delaying the formatting of certain fields
    """
    SEED = 1

    def __init__(self, value: str = EMPTY_STRING, prompt_args: PromptArgs = None,
                 response_manager: AbstractResponseManager = None):
        """
        Initialize with the value of the prompt
        :param value: The content of the prompt.
        :param prompt_args: The arguments defining the prompt.
        :param response_manager: Handles parsing responses from the LLM.
        """
        self.value = value
        self.args = prompt_args if prompt_args else PromptArgs()
        self.args.set_id(Prompt.SEED)
        self.response_manager = response_manager if response_manager else XMLResponseManager(include_response_instructions=False)
        Prompt.SEED += 1

    def build(self, partial_format_instructions: bool = False, **kwargs) -> str:
        """
        Builds the prompt in the correct format along with instructions for the response expected from the model
        :param kwargs: Any additional arguments for the prompt
        :param partial_format_instructions: If True, delays formatting of the response instructions.
        :return: The formatted prompt + instructions for the response expected from the model
        """
        structure = DictUtil.get_dict_values(kwargs, structure=self.args.structure_with_new_lines, pop=True)
        prompt = self._build(structure=structure, **kwargs)
        if response_instructions_variables := self.get_response_instruction_format_vars():
            format_var = DictUtil.get_key_by_index(response_instructions_variables)
            expected_response = response_instructions_variables[format_var]
            if partial_format_instructions:
                expected_response = StrUtil.get_format_symbol(format_var)
            prompt = f"{prompt}{SPACE}{expected_response}"
        return prompt

    def format_value(self, update_value: bool = True, *args: object, **kwargs: object) -> str:
        """
        A replacement for the string format to allow the formatting of only selective fields
        :param update_value: If True, updates the value permanently
        :param args: Ordered params to format the prompt with
        :param kwargs: Key, value pairs to format the prompt with
        :return: The formatted value
        """
        if not self.args.allow_formatting:
            return self.value
        value = StrUtil.format_selective(self.value, *args, **kwargs)
        if update_value:
            self.value = value
        return value

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the response from the model in the expected format for the prompt
        :param response: The model response
        :return: The formatted response
        """
        return self.response_manager.parse_response(response)

    def get_all_response_tags(self) -> List[str]:
        """
        Gets all response tags used in the response manager
        :return: All response tags used in the response manager
        """
        return self.response_manager.get_all_tag_ids()

    def structure_value(self, value: str = None, value_prefix: str = NEW_LINE, value_suffix: str = NEW_LINE):
        """
        Gets the value with any additional prefix or suffix added.
        :param value: The value to structure.
        :param value_prefix: Goes before the value.
        :param value_suffix: Goes after the value.
        :return: The value with any additional prefix or suffix added.
        """
        value = self.value if not value else value
        return f"{value_prefix}{value}{value_suffix}" if value else EMPTY_STRING

    def get_response_instruction_format_vars(self) -> dict:
        """
        Gets the format variables for the response instructions.
        :return: Dictionary mapping format var name to the response instructions to fill with.
        """
        return self.response_manager.get_response_instruction_format_vars(prompt_id=self.args.prompt_id)

    def _build(self, structure: bool = False, **kwargs) -> str:
        """
        Used to fulfill api, specific method of building for a prompt may be defined in child classes
        :param structure: If True, adds new lines before and after.
        :param kwargs: Any additional arguments for the prompt
        :return: The formatted prompt
        """
        update_value = DictUtil.get_dict_values(kwargs=kwargs, update_value=False, pop=True)
        value = self.format_value(update_value=update_value, **kwargs)
        if self.args.title:
            formatted_title = f"{PromptUtil.as_markdown_header(self.args.title)}"
            value = f"{formatted_title}{NEW_LINE}{value}" if value else formatted_title

        return value if not structure else self.structure_value(value)

    def __repr__(self) -> str:
        """
        Represents the prompt as a string
        :return: Represents the prompt as a string
        """
        return self.value
