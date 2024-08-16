from typing import List, Type, Union, Dict

from gen_common.llm.prompts.prompt_args import PromptArgs
from gen_common.llm.prompts.question_prompt import QuestionPrompt
from gen_common.llm.response_managers.abstract_response_manager import AbstractResponseManager
from gen_common.llm.response_managers.xml_response_manager import XMLResponseManager


class BinaryChoiceQuestionPrompt(QuestionPrompt):
    """
    Represents a Prompt that asks the model to select one of a two choices.
    """

    RESPONSE_INSTRUCTIONS1 = "Your answer should be {} or {} "
    RESPONSE_INSTRUCTIONS2 = "where {} {} and {} {}  "
    RESPONSE_TAG = "choice"

    def __init__(self, choices: Union[List, Dict], question: str, response_tag: str = None, prompt_args: PromptArgs = None,
                 response_manager_type: Type[AbstractResponseManager] = XMLResponseManager,
                 **additional_response_args):
        """
        Initializes the prompt with the categories that a model can select
        :param choices: A list of the choices available to the model
        :param question: The question being asked
        :param response_tag: The tag the model should enclose its response in
        :param default_factory: Method to define a default if response is not as expected
        :param prompt_args: The args to the base prompt.
        :param response_manager_type: The class of the reponse manager to use.
        :param additional_response_args: Any additional params to the response manager.
        """
        self.choices = list(choices.keys()) if isinstance(choices, dict) else choices
        response_instructions = self.RESPONSE_INSTRUCTIONS1.format(*choices)
        if isinstance(choices, dict):
            descr = []
            for item in choices.items():
                descr.extend(item)
            response_instructions += self.RESPONSE_INSTRUCTIONS2.format(*descr)
        response_instructions += response_manager_type.response_instructions_format
        response_tag = response_tag if response_tag else self.RESPONSE_TAG
        response_manager = response_manager_type(response_tag=response_tag,
                                                 response_instructions_format=response_instructions,
                                                 expected_responses={response_tag: self.choices},
                                                 expected_response_type={response_tag: type(self.choices[0])},
                                                 **additional_response_args)
        super().__init__(value=question, response_manager=response_manager, prompt_args=prompt_args)
