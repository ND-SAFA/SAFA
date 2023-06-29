import re
from abc import ABC, abstractmethod

from tgen.constants.deliminator_constants import NEW_LINE, EMPTY_STRING


class Prompt(ABC):
    """
    Represents a prompt with special formatting that allows delaying the formatting of certain fields
    """
    RESPONSE_FORMAT = "Enclose your answer inside of {}"

    def __init__(self, value: str, response_tag: str = None, include_expected_response: bool = True,
                 requires_traces: bool = False, requires_artifacts: bool = False):
        """
        Initialize with the value of the prompt
        :param value: The value of the prompt
        :param response_tag: The name of the tag the model is expected to enclose its response in
        :param include_expected_response: If True, includes the instructions for how the model should respond in the prompt
        """
        self.value = value
        self.response_tag = response_tag
        self.include_expected_response = include_expected_response
        self.requires_traces = requires_traces
        self.requires_artifacts = requires_artifacts

    def build(self, **kwargs) -> str:
        """
        Builds the prompt in the correct format along with instructions for the response expected from the model
        :param kwargs: Any additional arguments for the prompt
        :return: The formatted prompt + instructions for the response expected from the model
        """
        prompt = self._build(**kwargs)
        if self.include_expected_response:
            expected_response = self._build_expected_response()
            prompt = f"{prompt}{NEW_LINE}{expected_response}"
        return prompt

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

    @staticmethod
    def create_xml(tag_name: str, tag_content: str = EMPTY_STRING) -> str:
        """
        Creates xml as follows: <[tag_name]>tag_content</[tag_name]>
        :param tag_name: The name of the tag
        :param tag_content: The content inside of the tag
        :return: The formatted xml
        """
        return f"<{tag_name}>{tag_content}</{tag_name}>"

    def _build_expected_response(self) -> str:
        """
        Create the way the model should respond.
        :return: Formatted instructions for the response expected from the model
        """
        assert self.response_tag is not None, "Requires a response tag to be set in order to create instructions for model response"
        return self.RESPONSE_FORMAT.format(self.create_xml(tag_name=self.response_tag))

    def _build(self, **kwargs) -> str:
        """
        Specific method of building for a prompt (returns original value by default)
        :param kwargs: Any additional arguments for the prompt
        :return: The formatted prompt
        """
        return self.value