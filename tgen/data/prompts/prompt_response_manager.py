from dataclasses import field, dataclass
from typing import Union, Dict, Any, Callable, Type, List

from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.util.llm_response_util import LLMResponseUtil
from tgen.util.logging.logger_manager import logger
from tgen.util.prompt_util import PromptUtil
from tgen.util.str_util import StrUtil

RESPONSE_FORMAT = "Enclose your answer inside of {}"


@dataclass
class PromptResponseManager:
    """
    :param response_tag: The tag that the model uses to enclose its answer
    """
    response_tag: Union[str, dict]
    """
    :param response_instructions_format: The format of the instructions included in prompt to tell the model how to respond
    """
    response_instructions_format: str = RESPONSE_FORMAT
    """
    :param id2tag: A dictionary mapping the id of the tag to the tag name in order to fill in the response instructions with the 
                   appropriate tags
    """
    id2tag: Dict = field(default_factory=dict)
    """
    :param include_expected_response: If True, the response instructions will be automatically added to the prompt
    """
    include_response_instructions: bool = True
    """
    :param expected_response_type: A dictionary mapping the tag id to the expected response type for that tag
    """
    expected_response_type: Dict[str, Type] = field(default_factory=dict)
    """
    :param expected_responses: A dictionary mapping the tag id to the expected responses for that tag
    """
    expected_responses: Dict = field(default_factory=dict)
    """
    :param formatter: A method that takes in the tag id and returns the correct format for the associated response
    """
    formatter: Callable = None
    """
    :param default_factory: A method that takes in the tag id and returns a default failure for it if the response parsing fails
    """
    default_factory: Callable = None

    def __post_init__(self) -> None:
        """
        Converts input to the correct format after init
        :return: None
        """
        if not self.id2tag:
            if isinstance(self.response_tag, str):
                self.id2tag[self.response_tag] = self.response_tag
            else:
                for tag, children in self.response_tag.items():
                    self.id2tag[tag] = tag
                    for child in children:
                        self.id2tag[child] = child

    def format_response_instructions(self) -> str:
        """
        Formats the response instructions with the appropriate tags
        :return: The formatted response instructions
        """
        if not self.include_response_instructions:
            return EMPTY_STRING
        args = [PromptUtil.create_xml(tag_name=self.response_tag)] if isinstance(self.response_tag, str) else []
        kwargs = {id_: PromptUtil.create_xml(tag_name=tag) for id_, tag in self.id2tag.items()}
        return StrUtil.format_selective(self.response_instructions_format, *args, **kwargs)

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Used to fulfill api, may be overridden in child classes
        :param response: The model response
        :return: The response unchanged
        """
        output = {}
        if isinstance(self.response_tag, dict):
            for parent in self.response_tag.keys():
                output[parent] = LLMResponseUtil.parse(response, parent, is_nested=True, raise_exception=False)
        else:
            output[self.response_tag] = LLMResponseUtil.parse(response, self.response_tag, is_nested=False, raise_exception=False)
        return output

    def parse_response_on_failure(self, tag_id: str, e: Exception) -> Any:
        """
        Parses the response if it fails in some way, may be overridden in child classes
        :param tag_id: The id of the tag that failed
        :param e: The exception causing the failure
        :return: Default value
        """
        logger.warning(f"Unexpected response for {tag_id}: {e}.")
        if self.default_factory:
            return self.default_factory()
        return None

    def _format_response(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies the appropriate formatting to the response values for each tag
        :param output: Maps tag id to the parsed output from the model
        :return: A mapping of tag id to the formatted output value
        """
        formatted = {}
        for tag, val in output.items():
            if isinstance(val, dict):
                formatted[tag] = self._format_response(val)
            else:
                try:
                    formatted_val = val
                    if tag in self.expected_response_type:
                        formatted_val = self.expected_response_type[tag](formatted_val)
                    if self.formatter:
                        formatted_val = self.formatter(tag, formatted_val)
                    if tag in self.expected_responses:
                        assert formatted_val in self.expected_responses[tag]
                    formatted[tag] = formatted_val
                except (TypeError, AssertionError) as e:
                    formatted[tag] = self.parse_response_on_failure(tag, e)
        return formatted
