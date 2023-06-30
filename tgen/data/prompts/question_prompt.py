from typing import List, Callable, Any, Type

from tgen.data.prompts.prompt import Prompt
from tgen.util.logging.logger_manager import logger
from tgen.util.override import overrides


class QuestionPrompt(Prompt):
    """
    Represents a Prompt that asks the model a question
    """

    def __init__(self, question: str, response_tag: str = "answer", expected_responses: List = None,
                 expected_response_type: Type = str, default_factory: Callable = None,
                 response_instructions: str = Prompt.RESPONSE_FORMAT):
        """
        Initializes the prompt with the question that the model should answer
        :param question: The question the model should answer
        :param response_tag: The tags that the model should use in its response
        :param expected_responses: A list of all expected responses
        :param expected_response_type: The type to expect in the response
        :param default_factory: A function to call to replace value if response is unexpected
        :param response_instructions: The format instructions for the response desired from model
        """
        self.expected_responses = expected_responses
        self.expected_response_type = expected_response_type
        self.default_factory = default_factory
        super().__init__(value=question, response_tag=response_tag, response_instructions=response_instructions)

    @overrides(Prompt)
    def parse_response(self, response: Any) -> Any:
        """
        Parses the response for the prompt in the correct format and asserts that the response is as expected
        :param response: The response for the prompt
        :return: The parsed response
        """
        try:
            if not isinstance(response, self.expected_response_type):
                response = self.expected_response_type(response)
            if self.expected_responses:
                assert response in self.expected_responses
        except (TypeError, AssertionError) as e:
            response = self.parse_response_on_failure(response, e)
        return response

    @overrides(Prompt)
    def parse_response_on_failure(self, response: Any, e: Exception) -> Any:
        """
        Parses the response if it fails in some way
        :param response: The failed response
        :param e: The exception thrown
        :return: The default value to replace the response with
        """
        super().parse_response_on_failure(response, e)
        return self.default_factory(response) if self.default_factory else None
