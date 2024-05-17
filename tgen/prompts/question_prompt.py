from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.response_managers.abstract_response_manager import AbstractResponseManager


class QuestionPrompt(Prompt):
    """
    Represents a Prompt that asks the model a question
    """

    def __init__(self, value: str, prompt_args: PromptArgs = None, response_manager: AbstractResponseManager = None):
        """
        Initializes the prompt with the question that the model should answer
        :param value: The question the model should answer
        :param prompt_args: Additional args for the base prompt.
        :param response_manager: Handles creating response instructions and parsing response
        """
        super().__init__(value=value, prompt_args=prompt_args, response_manager=response_manager)
