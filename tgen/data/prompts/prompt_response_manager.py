import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Set, Type, Union

import bs4

from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.common.util.str_util import StrUtil
from tgen.constants.deliminator_constants import EMPTY_STRING

RESPONSE_FORMAT = "Enclose your answer inside of {}"
REQUIRE_ALL_TAGS = str(uuid.uuid4())


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
    :param required_tag_ids: A set of the tag ids that will throw an exception if not include
    """
    required_tag_ids: Union[Set, str] = field(default_factory=set)
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
            self._init_tag_attrs()
        self.expected_response_type = self._convert2dict(self.expected_response_type)
        self.expected_responses = self._convert2dict(self.expected_responses)
        if self.required_tag_ids == REQUIRE_ALL_TAGS:
            self.required_tag_ids = set(self._all_tag_ids)
        elif not isinstance(self.required_tag_ids, set):
            self.required_tag_ids = {self.required_tag_ids}

    def _convert2dict(self, initial_val: Any) -> Dict:
        """
        Converts a non-dict value to a dictionary mapping tag id to the given value to standardize a param
        :param initial_val: The original value which may not be a dictionary
        :return: A dictionary mapping tag id to a value
        """
        if not isinstance(initial_val, dict):
            return {id_: initial_val for id_ in self._all_tag_ids}
        return initial_val

    def _init_tag_attrs(self) -> None:
        """
        Initializes tag2id and all_tag_ids from the provided response tag and id2tag
        :return: None
        """
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
        args = [PromptUtil.create_xml(tag_name=tag) for tag in self.get_all_tag_ids()]
        kwargs = {id_: PromptUtil.create_xml(tag_name=tag) for id_, tag in self.id2tag.items()}
        return StrUtil.format_selective(self.response_instructions_format, *args, **kwargs)

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the response from the model in the expected format for the prompt
        :param response: The model response
        :return: The formatted response
        """
        if not self.response_tag:
            return {}
        output = {}
        if isinstance(self.response_tag, dict):
            for parent, child_tags in self.response_tag.items():
                values = LLMResponseUtil.parse(response, parent, is_nested=True, raise_exception=parent in self.required_tag_ids)
                values = [{self._tag2id[c_tag]: val.get(c_tag, None) for c_tag in child_tags} for val in values]
                output[self._tag2id[parent]] = values
        else:
            tags = [self.response_tag] if not isinstance(self.response_tag, list) else self.response_tag
            for tag in tags:
                tag_id = self._tag2id[tag]
                parsed = LLMResponseUtil.parse(response, tag, is_nested=False, raise_exception=tag in self.required_tag_ids)
                output[tag_id] = parsed if len(parsed) > 0 else [None]
        formatted_output = self._format_response(output)
        return formatted_output

    def _format_response(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies the appropriate formatting to the response values for each tag
        :param output: Maps tag id to the parsed output from the model
        :return: A mapping of tag id to the formatted output value
        """
        formatted = {}
        for tag, values in output.items():
            values = [values] if not isinstance(values, list) else values
            formatted_values = []
            for val in values:
                formatted_val = val
                if isinstance(val, dict):
                    formatted_values = self._format_response(val)
                else:
                    try:
                        assert val is not None, f"Missing {tag}"
                        if isinstance(formatted_val, bs4.NavigableString):
                            formatted_val = str(formatted_val)
                        if self.formatter:
                            formatted_val = self.formatter(tag, formatted_val)
                        is_list = isinstance(formatted_val, list)
                        vals2check = [formatted_val] if not is_list else formatted_val
                        if tag in self.expected_response_type:
                            vals2check = self._convert_to_expected_type(vals2check, tag, is_list)
                        if tag in self.expected_responses:
                            vals2check = self._assert_expected_response(vals2check, tag, is_list)
                        formatted_val = vals2check if is_list else vals2check.pop()
                    except (TypeError, AssertionError, ValueError) as e:
                        formatted_val = self._format_on_failure(tag, formatted_val, e)
                    formatted_values.append(formatted_val)
            formatted[tag] = formatted_values
        return formatted

    def _assert_expected_response(self, vals2check: List[Any], tag: str, is_list: bool) -> List[Any]:
        """
        Asserts that all values are expected
        :param vals2check: The values to check
        :param tag: The tag used to output values
        :param is_list: True if the response is a list
        :return: The checked values
        """
        checked_values = []
        for v in vals2check:
            val = v
            if v not in self.expected_responses[tag]:
                val = self._format_on_failure(tag, v, AssertionError(f"Unexpected value for {tag}"),
                                              no_exception=is_list, return_none_on_fail=is_list)
            if val is not None:
                checked_values.append(val)
        return checked_values

    def _convert_to_expected_type(self, vals2convert: List[Any], tag: str, is_list: bool) -> List[Any]:
        """
        Returns the list of values converted to the expected type
        :param vals2convert: The list of values to convert
        :param tag: The tag used to output values
        :return: The list of converted values
        """
        converted = []
        for v in vals2convert:
            try:
                val = self.expected_response_type[tag](v)
            except (ValueError, TypeError) as e:
                val = self._format_on_failure(tag, v, e, no_exception=is_list, return_none_on_fail=is_list)
            if val is not None:
                converted.append(val)
        return converted

    def _format_on_failure(self, tag_id: str, val: Any, e: Union[Exception, str], no_exception: bool = False,
                           return_none_on_fail: bool = False) -> Any:
        """
        Parses the response if it fails in some way, may be overridden in child classes
        :param tag_id: The id of the tag that failed
        :param e: The exception causing the failure
        :param no_exception: If True, no exception will be thrown
        :param return_none_on_fail: If True, returns None instead of the origin value
        :return: Default value
        """
        assert no_exception or tag_id not in self.required_tag_ids, f"Missing expected tag {tag_id}"
        logger.warning(f"Unexpected response for {tag_id}: {e}.")
        if self.default_factory:
            return self.default_factory(tag_id, val)
        return val if not return_none_on_fail else None
