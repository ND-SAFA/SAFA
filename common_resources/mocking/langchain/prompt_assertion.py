from typing import Callable, List, Type, Dict, Optional

from pydantic.v1.main import BaseModel

from common_resources_test.base_tests.base_test import BaseTest


class PromptAssertion:

    def __init__(self, assertion: Callable | List[Callable], response: str | BaseModel):
        """
        Handles checking a prompt is expected and mocking the response for testing.
        :param assertion: Method(s) to assert prompt is good.
        :param response: The mocked response
        """
        self.assertions: List[Callable] = assertion if isinstance(assertion, list) else [assertion]
        self.response = response

    def run_assertions(self, *args, **kwargs) -> None:
        """
        Runs all assertions on the params.
        :param args: Args to the fake LLM.
        :param kwargs: Kwargs to the fake LLM.
        :return: None
        """
        for assertion in self.assertions:
            assertion(*args, **kwargs)

    def __call__(self, *args, **kwargs) -> str | BaseModel:
        """
        Checks prompt and returns mock response
        :param args: Args to the fake LLM.
        :param kwargs: Kwargs to the fake LLM.
        :return: The mocked response.
        """
        self.run_assertions(*args, **kwargs)
        return self.response


class AssertInPrompt:

    def __init__(self, test_case: BaseTest, value: str, in_system_prompt: bool = False, message_number: int = None):
        """
        Represents a prompt assertion to test if some text is in system or message prompt or to assert that it is not there.
        :param test_case: The test case being run.
        :param in_system_prompt: If True, checks for text in system prompt, else checks that it is not there.
        :param message_number: If True, checks for text in message prompt, else checks that it is not there.
        :param value: The value to check for.
        """
        self.test_case = test_case
        self.in_system_prompt = in_system_prompt
        self.message_number = message_number
        self.value = value

    def run_assertion(self, *args, **kwargs) -> None:
        """
        Asserts that some text is in system or message prompt or to assert that it is not there.
        :param args: Args to the LLM.
        :param kwargs: Kwargs to the LLM.
        :return: None
        """
        system_prompt = kwargs.get("system")
        if self.in_system_prompt:
            self.test_case.assertIn(self.value, system_prompt)

        if self.message_number is not None:
            message_prompt = kwargs.get("messages")[self.message_number]["content"]
            self.test_case.assertIn(self.value, message_prompt)

    def __call__(self, *args, **kwargs):
        self.run_assertion(*args, **kwargs)


class AssertToolAvailable:

    def __init__(self, test_case: BaseTest, tool: Type[BaseModel], is_expected_to_be_available: bool = True):
        """
        Represents a prompt assertion to test if some text is in system or message prompt or to assert that it is not there.
        :param test_case: The test case being run.
        :param tool: Tool to run assertion for.
        :param is_expected_to_be_available: If True, checks for tool, else checks that it is not there.
        """
        self.test_case = test_case
        self.is_expected_to_be_available = is_expected_to_be_available
        self.tool = tool

    def run_assertion(self, *args, **kwargs) -> None:
        """
        Asserts that a tool is given to the model.
        :param args: Args to the LLM.
        :param kwargs: Kwargs to the LLM.
        :return: None
        """
        tool_val = self.get_tool(self.tool, kwargs.get("tools"))
        if self.is_expected_to_be_available:
            self.test_case.assertIsNotNone(tool_val, msg=f"Missing Tool {self.tool.__name__}")
        else:
            self.test_case.assertIsNone(tool_val, msg=f"Found Unexpected Tool {self.tool.__name__}")

    @staticmethod
    def get_tool(tool: Type[BaseModel], tools: List[Dict]) -> Optional[Dict]:
        """
        Gets a tool from the args to the model.
        :param tool: The tool to look for.
        :param tools: All tools.
        :return: The tool if it exists.
        """
        filtered_tools = [t for t in tools if t["name"] == tool.__name__]
        if filtered_tools:
            return filtered_tools[0]

    def __call__(self, *args, **kwargs):
        self.run_assertion(*args, **kwargs)
