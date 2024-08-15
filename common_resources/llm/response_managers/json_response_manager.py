import json
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Type

from common_resources.llm.response_managers.abstract_response_manager import AbstractResponseManager
from common_resources.tools.util.dict_util import DictUtil
from common_resources.tools.util.json_util import JsonUtil

RESPONSE_FORMAT = "You should respond using the following JSON format:\n{}"


@dataclass
class JSONResponseManager(AbstractResponseManager):
    """
    :param response_instructions_format: The format of the instructions included in prompt to tell the model how to respond
    """
    response_instructions_format: str = RESPONSE_FORMAT

    def __init__(self, **kwargs):
        """
        Ensures proper super attrs are overridden.
        :param kwargs: The params to the response manager.
        """
        kwargs = DictUtil.update_kwarg_values(kwargs,
                                              response_instructions_format=JSONResponseManager.response_instructions_format,
                                              replace_existing=False)
        super().__init__(**kwargs)

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the response from the model in the expected format for the prompt
        :param response: The model response
        :return: The formatted response
        """
        if not self.response_tag:
            return {}
        response_dict = json.loads(response)
        output = self._parse_response_helper(response_dict)
        return self._format_response(output)

    def _parse_response_helper(self, response: Any, response_tags: Any = None) -> Any:
        """
        Parses the JSON response.
        :param response: The response as a native python object.
        :param response_tags: The expected tags/format.
        :return: The parsed response.
        """
        response_tags = self.response_tag if not response_tags else response_tags
        output = {}
        if isinstance(response_tags, dict):
            self._assert_response_format(response, response_tags, dict)
            for parent, children in response_tags.items():
                if parent not in response:
                    if parent in self.required_tag_ids:
                        raise KeyError(f"Missing {parent} in response.")
                    parsed_children = None
                else:
                    parsed_children = self._parse_response_helper(response[parent], children)
                output[self._tag2id[parent]] = [parsed_children] if not isinstance(parsed_children, list) else parsed_children
            return output
        elif isinstance(response_tags, list):
            self._assert_response_format(response, response_tags, list)
            return [self._parse_response_helper(v, response_tags[0]) for v in response]
        else:
            return response

    def _collect_all_tags(self) -> List[str]:
        """
        Collects all response tags used.
        :return: a list of all response tags that are used.
        """
        if not self.response_tag and self.tag_descriptions:
            self.response_tag = self.tag_descriptions
        elif isinstance(self.response_tag, str):
            self.response_tag = {self.response_tag: self.tag_descriptions.get(self.response_tag, self.response_tag)}
        all_tags = JsonUtil.get_all_fields(self.response_tag)
        return all_tags

    @staticmethod
    def _assert_response_format(response: Any, expected: Any, expected_type: Type) -> None:
        """
        Ensures the response is in the expected format.
        :param response: The response:
        :param expected: Expected response format.
        :param expected_type: Format type.
        :return: None
        """
        assert isinstance(response, expected_type), f"Response not in correct format: \nexpected {expected}, \nreceived {response}"

    def _get_response_instructions_format_params(self) -> Tuple[List, Dict]:
        """

        :return: The args and kwargs needed for the response instructions format.
        """
        args = [JsonUtil.dict_to_json(self.response_tag)]
        kwargs = {}
        return args, kwargs
