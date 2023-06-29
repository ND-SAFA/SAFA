from enum import StrEnum, auto
from typing import Dict, Callable, List

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.util.override import overrides


class BinaryChoiceQuestionPrompt(QuestionPrompt):
    """
    Represents a Prompt that asks the model to select one of a two choices.
    """

    RESPONSE_INSTRUCTIONS1 = "Your answer should be {} or {}."
    RESPONSE_INSTRUCTIONS2 = "Enclose your choice inside of {}"
    RESPONSE_TAG = "choice"

    def __init__(self, choices: List, question: str, response_tag: str = None, default_factory: Callable = None):
        """
        Initializes the prompt with the categories that a model can select
        :param choices: A list of the choices available to the model
        :param question: The question being asked
        :param response_tag: The tag the model should enclose its response in
        :param default_factory: Method to define a default if response is not as expected
        """
        self.choices = choices
        response_instructions = f"{self.RESPONSE_INSTRUCTIONS1.format(*choices)} {self.RESPONSE_INSTRUCTIONS2}"
        super().__init__(question=question,
                         response_tag=response_tag if response_tag else self.RESPONSE_TAG,
                         expected_responses=self.choices, response_instructions=response_instructions,
                         expected_response_type=type(choices[0]), default_factory=default_factory)
