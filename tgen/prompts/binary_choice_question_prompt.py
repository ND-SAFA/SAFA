from typing import List

from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager


class BinaryChoiceQuestionPrompt(QuestionPrompt):
    """
    Represents a Prompt that asks the model to select one of a two choices.
    """

    RESPONSE_INSTRUCTIONS1 = "Your answer should be {} or {}."
    RESPONSE_INSTRUCTIONS2 = "Enclose your choice inside of {}"
    RESPONSE_TAG = "choice"

    def __init__(self, choices: List, question: str, response_tag: str = None, prompt_args: PromptArgs = None,
                 **additional_response_args):
        """
        Initializes the prompt with the categories that a model can select
        :param choices: A list of the choices available to the model
        :param question: The question being asked
        :param response_tag: The tag the model should enclose its response in
        :param default_factory: Method to define a default if response is not as expected
        :param prompt_args: The args to the base prompt.
        :param additional_response_args: Any additional params to the response manager.
        """
        self.choices = choices
        response_instructions = f"{self.RESPONSE_INSTRUCTIONS1.format(*choices)} {self.RESPONSE_INSTRUCTIONS2}"
        response_tag = response_tag if response_tag else self.RESPONSE_TAG
        response_manager = XMLResponseManager(response_tag=response_tag,
                                              response_instructions_format=response_instructions,
                                              expected_responses={response_tag: self.choices},
                                              expected_response_type={response_tag: type(choices[0])},
                                              **additional_response_args)
        super().__init__(value=question, response_manager=response_manager, prompt_args=prompt_args)
