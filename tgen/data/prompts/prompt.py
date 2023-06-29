import re
import uuid
from abc import ABC, abstractmethod
from typing import Any

from tgen.constants.deliminator_constants import NEW_LINE, EMPTY_STRING
from tgen.util.llm_response_util import LLMResponseUtil
from tgen.util.logging.logger_manager import logger
from tgen.util.prompt_util import PromptUtil


class Prompt(ABC):
    """
    Represents a prompt with special formatting that allows delaying the formatting of certain fields
    """
    RESPONSE_FORMAT = "Enclose your answer inside of {}"

    def __init__(self, value: str, response_tag: str = None, prompt_id: str = None, include_expected_response: bool = True,
                 requires_traces: bool = False, requires_artifacts: bool = False, response_instructions: str = RESPONSE_FORMAT):
        """
        Initialize with the value of the prompt
        :param value: The value of the prompt
        :param response_tag: The name of the tag the model is expected to enclose its response in
        :param prompt_id: Specify specific id for the prompt
        :param include_expected_response: If True, includes the instructions for how the model should respond in the prompt
        :param requires_traces: True if prompt requires trace link
        :param requires_artifacts: True if prompt requires artifacts
        :param response_instructions: The format instructions for the response desired from model
        """
        self.value = value
        self.id = prompt_id if prompt_id is not None else str(uuid.uuid4())
        self.response_tag = response_tag
        self.include_expected_response = include_expected_response
        self.requires_traces = requires_traces
        self.requires_artifacts = requires_artifacts
        self.response_instructions = response_instructions

    def build(self, **kwargs) -> str:
        """
        Builds the prompt in the correct format along with instructions for the response expected from the model
        :param kwargs: Any additional arguments for the prompt
        :return: The formatted prompt + instructions for the response expected from the model
        """
        prompt = self._build(**kwargs)
        if self.include_expected_response:
            expected_response = self._build_response_instructions()
            prompt = f"{prompt}{NEW_LINE}{expected_response}"
        return prompt

    def parse_response(self, response: str) -> Any:
        """
        Used to fulfill api, may be overridden in child classes
        :param response: The model response
        :return: The response unchanged
        """
        return response

    def parse_response_on_failure(self, response: str, e: Exception) -> Any:
        """
        Parses the response if it fails in some way, may be overridden in child classes
        :param response: The model response
        :return: Default value
        """
        logger.warning(f"Unexpected response for {self.value} because {e}.")
        return None

    def format_value(self, *args: object, **kwargs: object) -> None:
        """
        A replacement for the string format to allow the formatting of only selective fields
        :param args: Ordered params to format the prompt with
        :param kwargs: Key, value pairs to format the prompt with
        :return: None
        """
        formatting_fields = re.findall(r'\{(\w*)\}', self.value)
        updated_args = [arg for arg in args]
        for i, field in enumerate(formatting_fields):
            if kwargs and field not in kwargs:
                kwargs[field] = '{%s}' % field
            if args and i >= len(args):
                updated_args.append('{%s}' % field)
        self.value = self.value.format(*updated_args, **kwargs)

    def _build_response_instructions(self) -> str:
        """
        Create the instructions for how the model should respond.
        :return: Formatted instructions for the response expected from the model
        """
        assert self.response_tag is not None, "Requires a response tag to be set in order to create instructions for model response"
        return self.response_instructions.format(PromptUtil.create_xml(tag_name=self.response_tag))

    def _build(self, **kwargs) -> str:
        """
        Used to fulfill api, specific method of building for a prompt may be defined in child classes
        :param kwargs: Any additional arguments for the prompt
        :return: The formatted prompt
        """
        return self.value
