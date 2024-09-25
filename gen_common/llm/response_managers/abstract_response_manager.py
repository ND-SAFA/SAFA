import logging
import uuid
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Set, Tuple, Type, Union

import bs4
from langchain_core.pydantic_v1 import BaseModel, Field

from gen_common.constants.symbol_constants import DASH, EMPTY_STRING
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.util.str_util import StrUtil

RESPONSE_FORMAT = "Enclose your answer inside of {}"
USE_ALL_TAGS = str(uuid.uuid4())


@dataclass
class AbstractResponseManager:
    """
    :param response_tag: The tag that the model uses to enclose its answer
    """
    response_tag: Union[str, dict, list] = EMPTY_STRING
    """
    :param parse_all: Whether the entire response should be parsed by response manager.
    """
    parse_all: bool = False
    """
    :param tag_descriptions: Maps tag id to its description.
    """
    tag_descriptions: Dict[str, str] = field(default_factory=dict)
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
    expected_responses: Union[List, Dict[str, Set]] = field(default_factory=dict)
    """
    :param formatter: A method that takes in the tag id and returns the correct format for the associated response
    """
    value_formatter: Callable = None
    """
    :param default_factory: A method that takes in the tag id and returns a default failure for it if the response parsing fails
    """
    default_factory: Callable = None
    """
    :param required_tag_ids: A set of the tag ids that will throw an exception if not include
    """
    required_tag_ids: Union[Set, str] = field(default_factory=set)
    """
    :param required_tag_ids: A set of the tag ids that will not even log when missing because it is expected
    """
    optional_tag_ids: Union[Set, str] = field(default_factory=set)
    """
    Formats an entry given its tag and values.
    """
    entry_formatter: Callable[[str, Dict], Any] = None
    """
    If True, will convert the response to one of the expected responses if it is sufficiently close.
    """
    loose_response_validation: bool = False
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
    """
    The id of the response manager.
    """
    _r_id: uuid.UUID = field(init=False, default_factory=uuid.uuid4)
    """
    The langgraph model class.
    """
    _model: BaseModel = field(init=False, default=None)

    def __post_init__(self) -> None:
        """
        Converts input to the correct format after init
        :return: None
        """
        if self.response_tag or self.tag_descriptions:
            self._init_tag_attrs()
        self.expected_response_type = self._convert2dict(self.expected_response_type)
        self.expected_responses = self._convert2dict(self.expected_responses)
        self.required_tag_ids = self._post_process_tag_id_sets(self.required_tag_ids)
        self.optional_tag_ids = self._post_process_tag_id_sets(self.optional_tag_ids)
        if self.get_all_tag_ids():
            self._r_id = DASH.join(self.get_all_tag_ids())

    def get_response_instruction_format_vars(self, prompt_id: str) -> Dict:
        """
        Gets the format variables for the response instructions.
        :param prompt_id: ID of the prompt to get the format variables for.
        :return: Dictionary mapping format var name to the response instructions to fill with.
        """
        if response_instructions := self.format_response_instructions():
            return {f"format_instructions_{prompt_id}": response_instructions}
        return dict()

    def get_langgraph_model(self) -> Type[BaseModel]:
        """
        Converts the expected response into a langgraph model.
        :return: The langgraph model.
        """
        if self._model is None:
            class_attributes = {
                tag_id: Field(description=self.tag_descriptions.get(tag_id, tag_id)) for tag, tag_id in self._tag2id.items()
            }
            class_attributes["__annotations__"] = {tag_id: self.expected_response_type.get(tag_id, str) for tag_id in class_attributes}

            # Dynamically create the class
            ResponseModel = type(f"ResponseModel{str(self._r_id)}", (BaseModel,), class_attributes)
            self._model = ResponseModel
        return self._model

    @classmethod
    def from_langgraph_model(cls, model: BaseModel, **additional_params) -> "AbstractResponseManager":
        """
        Creates a response manager based on the langgraph model.
        :param model: The langgraph model.
        :param additional_params: Additional params to the response manager.
        :return: The response manager based on the langgraph model.
        """
        tags = model.__fields__
        response_manager = cls(
            tag_descriptions={name: tag.field_info.description for name, tag in tags.items()},
            expected_response_type={name: tag.type_ for name, tag in tags.items()},
            **additional_params)
        response_manager._model = model
        return response_manager

    def response_as_langgraph_model(self, parsed_response: Dict[str, Any]) -> BaseModel:
        """
        Constructs a langgraph model obj from the response.
        :param parsed_response: The parsed response from the model.
        :return: Langgraph model obj constructed from the response
        """
        return self.get_langgraph_model()(**parsed_response)

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
        args, kwargs = self._get_response_instructions_format_params()
        return StrUtil.format_selective(self.response_instructions_format, *args, **kwargs)

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the response from the model in the expected format for the prompt
        :param response: The model response
        :return: The formatted response
        """
        if not self.parse_all and not self.response_tag:
            return {}
        return self._parse_response(response)

    def _post_process_tag_id_sets(self, tag_ids: Union[Set, str]) -> Set[str]:
        """
        Performs necessary post-processing on required and optional tag ids set to ensure they are in correct format.
        :param tag_ids: The required or optional tag ids set to post-process.
        :return: Correctly formatted set of tag ids for required and optional tag ids set.
        """
        if tag_ids == USE_ALL_TAGS:
            tag_ids = set(self.get_all_tag_ids())
        elif not isinstance(tag_ids, set):
            tag_ids = {tag_ids}
        return tag_ids

    def _convert2dict(self, initial_val: Any) -> Dict:
        """
        Converts a non-dict value to a dictionary mapping tag id to the given value to standardize a param
        :param initial_val: The original value which may not be a dictionary
        :return: A dictionary mapping tag id to a value
        """
        if not isinstance(initial_val, dict):
            return {id_: initial_val for id_ in self.get_all_tag_ids()}
        return initial_val

    def _init_tag_attrs(self) -> None:
        """
        Initializes tag2id and all_tag_ids from the provided response tag and id2tag
        :return: None
        """
        all_tags = self._collect_all_tags()
        ids = set(self.id2tag.values())
        for tag in all_tags:
            if tag not in ids:
                self.id2tag[tag] = tag
        self._tag2id = {tag: id_ for id_, tag in self.id2tag.items()}
        self._all_tag_ids = [self._tag2id.get(tag, tag) for tag in all_tags]

    def _format_response(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies the appropriate formatting to the response values for each tag
        :param output: Maps tag id to the parsed output from the model
        :return: A mapping of tag id to the formatted output value
        """
        formatted_tags = {}
        for tag, values in output.items():
            values, _ = self._convert2list(values)
            formatted_values = []
            for val in values:
                formatted_val = val
                if isinstance(val, dict):
                    formatted_val = self._format_response(val)
                    if self.entry_formatter:
                        try:
                            formatted_val = self.entry_formatter(tag, formatted_val)
                        except Exception:
                            logger.exception("Received exception while attempting to format response.")
                    formatted_values.append(formatted_val)
                else:
                    try:
                        formatted_val = self._format_value(tag, formatted_val)
                    except (TypeError, AssertionError, ValueError) as e:
                        if tag not in self.optional_tag_ids:
                            logger.log_without_spam(level=logging.ERROR, msg=str(e))
                        formatted_val = self._format_on_failure(tag, formatted_val, e)
                    if formatted_val is not None:
                        formatted_values.append(formatted_val)
            formatted_tags[tag] = formatted_values
        return formatted_tags

    def _format_value(self, tag: str, orig_val: Any) -> Any:
        """
        Formats a value for a tag
        :param tag: The tag to format the value for
        :param orig_val: The original value
        :return: The formatted value
        """
        assert orig_val is not None, f"{orig_val} is missing {tag}"
        vals2format, orig_vals_is_list = self._convert2list(orig_val)
        formatted = []
        for val in vals2format:
            if isinstance(val, bs4.NavigableString):
                val = str(val)
            if self.value_formatter:
                val = self.value_formatter(tag, val)
            inner_vals, inner_vals_is_list = self._convert2list(val)
            if tag in self.expected_response_type:
                inner_vals = self._convert_to_expected_type(inner_vals, tag, inner_vals_is_list)
            if tag in self.expected_responses:
                inner_vals = self._assert_expected_response(inner_vals, tag, inner_vals_is_list)
            val = inner_vals if inner_vals_is_list else inner_vals.pop()
            if val is not None:
                formatted.append(val)
        formatted_val = formatted if orig_vals_is_list else formatted.pop()
        return formatted_val

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
            success = False
            if isinstance(self.expected_responses[tag], range):
                expected_range = sorted(list(self.expected_responses[tag]))
                if expected_range[0] <= v <= expected_range[-1]:
                    success = True
            elif v in self.expected_responses[tag]:
                success = True
            if not success:
                closest_val = []
                if self.loose_response_validation:
                    try:
                        expected_response_order = list(self.expected_responses[tag])
                        lower_cased_expected = [r.lower() for r in expected_response_order if isinstance(r, str)]
                        lower_case_v = v.strip().lower() if isinstance(v, str) else v
                        index = lower_cased_expected.index(lower_case_v)
                        closest_val.append(expected_response_order[index])
                    except ValueError:
                        closest_val = [r for r in self.expected_responses[tag] if
                                       hasattr(r, '__contains__') and r in v] if self.loose_response_validation else []
                if len(closest_val) == 1:
                    success = True
                    val = closest_val[0]
                else:
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
        :param is_list: If true no exception is thrown if formatting error occurs.
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
        :param val: The value of the prompt.
        :param e: The exception causing the failure
        :param no_exception: If True, no exception will be thrown
        :param return_none_on_fail: If True, returns None instead of the origin value
        :return: Default value
        """
        assert no_exception or tag_id not in self.required_tag_ids, f"Missing expected tag {tag_id}"
        if tag_id not in self.optional_tag_ids:
            logger.log_without_spam(level=logging.WARNING, msg=f"Unexpected response for {tag_id}: {val} - {e}.")
        if self.default_factory:
            return self.default_factory(tag_id, val)
        return val if not return_none_on_fail else None

    @staticmethod
    def _convert2list(orig_val: Any) -> Tuple[List, bool]:
        """
        Converts val to list if not already
        :param orig_val: The original value
        :return: The values as a list and whether it was already a list
        """
        is_list = isinstance(orig_val, list)
        return [orig_val] if not is_list else orig_val, is_list

    @abstractmethod
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the response from the model in the expected format for the prompt
        :param response: The model response
        :return: The formatted response
        """

    @abstractmethod
    def _get_response_instructions_format_params(self) -> Tuple[List, Dict]:
        """
        Gets the args and kwargs needed to format the response instructions.
        :return: The args and kwargs needed for the response instructions format.
        """

    @abstractmethod
    def _collect_all_tags(self) -> List[str]:
        """
        Collects all response tags used.
        :return: a list of all response tags that are used.
        """

    def __eq__(self, other: "AbstractResponseManager") -> bool:
        """
        Checks if two response managers are the same.
        :param other: The other object.
        :return: True if two response managers are the same.
        """
        return self._r_id == getattr(other, "_r_id", None)
