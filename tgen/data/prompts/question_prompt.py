from typing import List, Callable, Any, Type

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager


class QuestionPrompt(Prompt):
    """
    Represents a Prompt that asks the model a question
    """

    def __init__(self, question: str, response_manager: PromptResponseManager):
        """
        Initializes the prompt with the question that the model should answer
        :param question: The question the model should answer
        :param response_manager: Handles creating response instructions and parsing response
        """
        super().__init__(value=question, response_manager=response_manager)
