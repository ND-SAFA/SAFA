import uuid

from typing import Dict, Any

from tgen.constants.deliminator_constants import NEW_LINE, SPACE
from tgen.data.prompts.prompt_response_manager import RESPONSE_FORMAT, PromptResponseManager
from tgen.util.str_util import StrUtil


class Prompt:
    """
    Represents a prompt with special formatting that allows delaying the formatting of certain fields
    """

    def __init__(self, value: str, response_manager: PromptResponseManager = None, prompt_id: str = None):
        """
        Initialize with the value of the prompt
        :param value: The value of the prompt
        :param response_manager: Handles creating response instructions and parsing response
        :param prompt_id: Specify specific id for the prompt
        """
        self.value = value
        self.id = prompt_id if prompt_id is not None else str(uuid.uuid4())
        self.response_manager = response_manager if response_manager else PromptResponseManager(include_response_instructions=False)

    def build(self, **kwargs) -> str:
        """
        Builds the prompt in the correct format along with instructions for the response expected from the model
        :param kwargs: Any additional arguments for the prompt
        :return: The formatted prompt + instructions for the response expected from the model
        """
        prompt = self._build(**kwargs)
        expected_response = self.response_manager.format_response_instructions()
        if expected_response:
            prompt = f"{prompt}{SPACE}{expected_response}"
        return prompt

    def format_value(self, *args: object, **kwargs: object) -> None:
        """
        A replacement for the string format to allow the formatting of only selective fields
        :param args: Ordered params to format the prompt with
        :param kwargs: Key, value pairs to format the prompt with
        :return: None
        """
        self.value = StrUtil.format_selective(self.value, *args, **kwargs)

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the response from the model in the expected format for the prompt
        :param response: The model response
        :return: The formatted response
        """
        return self.response_manager.parse_response(response)

    def _build(self, **kwargs) -> str:
        """
        Used to fulfill api, specific method of building for a prompt may be defined in child classes
        :param kwargs: Any additional arguments for the prompt
        :return: The formatted prompt
        """
        self.format_value(**kwargs)
        return self.value

    def __repr__(self) -> str:
        """
        Represents the prompt as a string
        :return: Represents the prompt as a string
        """
        return self.value
