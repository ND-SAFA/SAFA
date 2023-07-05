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
    response_tag: Union[str, dict, list] = EMPTY_STRING
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
    expected_response_type: Union[Type, Dict[str, Type]] = field(default_factory=dict)
    """
    :param expected_responses: A dictionary mapping the tag id to the expected responses for that tag
    """
    expected_responses: Union[List, Dict[str, List]] = field(default_factory=dict)
    """
    :param formatter: A method that takes in the tag id and returns the correct format for the associated response
    """
    formatter: Callable = None
    """
    :param default_factory: A method that takes in the tag id and returns a default failure for it if the response parsing fails
    """
    default_factory: Callable = None

    """
    Create reverse lookup for tags to their ids after init
    """
    _tag2id: Dict[str, str] = field(init=False, default_factory=dict)
    """
    A list of all response tags in the order they are provided . 
     If parent, children, they are returned in the order:
     p1, c1.1, .. c1.n, p2, c2.1, .. c2.n,... pn, cn.1, .. cn.n
    """
    _all_tag_ids: List[str] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        """
        Converts input to the correct format after init
        :return: None
        """
        if self.response_tag:
            all_tags = []
            if isinstance(self.response_tag, str):
                all_tags.append(self.response_tag)
            elif isinstance(self.response_tag, list):
                all_tags.extend(self.response_tag)
            else:
                for tag, children in self.response_tag.items():
                    all_tags.append(tag)
                    all_tags.extend(children)
            if not self.id2tag:
                self.id2tag = {tag: tag for tag in all_tags}
            self._tag2id = {tag: id_ for id_, tag in self.id2tag.items()}
            self._all_tag_ids = [self._tag2id[tag] for tag in all_tags]

    def get_all_tag_ids(self) -> List[str]:
        """
        Gets all the response tag ids in the order they are provided .
        If parent, children, they are returned in the order:
        p1, c1.1, .. c1.n, p2, c2.1, .. c2.n,... pn, cn.1, .. cn.n
        :return: All the response tag ids in the order they are provided
        """
        return self._all_tag_ids

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
        if not self.response_tag:
            return {}
        output = {}
        if isinstance(self.response_tag, dict):
            for parent in self.response_tag.keys():
                values = LLMResponseUtil.parse(response, parent, is_nested=True, raise_exception=False)
                values = [{self._tag2id.get(c_id, c_id): c_val for c_id, c_val in val.items()} for val in values]
                output[self._tag2id[parent]] = values
        else:
            tags = [self.response_tag] if not isinstance(self.response_tag, list) else self.response_tag
            for tag in tags:
                tag_id = self._tag2id[tag]
                output[tag_id] = LLMResponseUtil.parse(response, tag, is_nested=False, raise_exception=False)
        formatted_output = self._format_response(output)
        return formatted_output

    def get_expected_response_type(self, tag: str) -> Type:
        """
        Gets the expected response type for a tag
        :param tag: The id of the tag
        :return:
        """
        if isinstance(self.expected_response_type, dict):
            if tag in self.expected_response_type:
                return self.expected_response_type[tag]
        else:
            return self.expected_response_type

    def get_expected_responses(self, tag: str) -> List:
        """
        Gets the expected responses for a tag
        :param tag: the id of the tag
        :return: The expected responses
        """
        if isinstance(self.expected_responses, dict):
            if tag in self.expected_responses:
                return self.expected_responses[tag]
        else:
            return self.expected_responses

    def _format_response(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies the appropriate formatting to the response values for each tag
        :param output: Maps tag id to the parsed output from the model
        :return: A mapping of tag id to the formatted output value
        """
        formatted = {}
        for tag, values in output.items():
            if not isinstance(values, list):
                values = [values]
            formatted_values = []
            for val in values:
                formatted_val = val
                if isinstance(val, dict):
                    formatted_val = self._format_response(val)
                else:
                    try:
                        expected_response_type = self.get_expected_response_type(tag)
                        if expected_response_type:
                            formatted_val = expected_response_type(formatted_val)
                        if self.formatter:
                            formatted_val = self.formatter(tag, formatted_val)
                        expected_response = self.get_expected_responses(tag)
                        if expected_response:
                            assert formatted_val in self.expected_responses[tag]
                    except (TypeError, AssertionError) as e:
                        formatted_val = self._format_on_failure(tag, formatted_val, e)
                formatted_values.append(formatted_val)
            formatted[tag] = formatted_values
        return formatted

    def _format_on_failure(self, tag_id: str, val: Any, e: Exception) -> Any:
        """
        Parses the response if it fails in some way, may be overridden in child classes
        :param tag_id: The id of the tag that failed
        :param e: The exception causing the failure
        :return: Default value
        """
        logger.warning(f"Unexpected response for {tag_id}: {e}.")
        if self.default_factory:
            return self.default_factory(tag_id, val)
        return val

