from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager


class QuestionPrompt(Prompt):
    """
    Represents a Prompt that asks the model a question
    """

    def __init__(self, value: str, response_manager: PromptResponseManager = None):
        """
        Initializes the prompt with the question that the model should answer
        :param value: The question the model should answer
        :param response_manager: Handles creating response instructions and parsing response
        """
        super().__init__(value=value, response_manager=response_manager)
