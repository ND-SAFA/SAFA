from string import ascii_uppercase
from typing import List

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.util.override import overrides


class QuestionnairePrompt(Prompt):
    """
    Contains a list of questions for the model to answer
    """

    def __init__(self, question_prompts: List[QuestionPrompt], instructions: str = "", enumeration_chars: List[str] = ascii_uppercase):
        """
        Initializes the questionairre with the instructions and the questions that will make up the prompt
        :param question_prompts: The list of question prompts to include in the questionairre
        :param instructions: Any instructions necessary with the questionairre
        :param enumeration_chars: The list of characters to use to enumerate the questions (must include one for each question)
        """
        self.question_prompts = question_prompts
        self.enumeration_chars = enumeration_chars
        response_manager = PromptResponseManager(response_tag=[prompt.response_manager.response_tag for prompt in self.question_prompts],
                                                 include_response_instructions=False)
        super().__init__(instructions, response_manager=response_manager)

    @overrides(Prompt)
    def _build(self, **kwargs) -> str:
        """
        Constructs the prompt in the following format:
        [Instructions]
        A) Question 1
        B) ...
        C) Question n
        :return: The formatted prompt
        """
        self.format_value(**kwargs)
        question_format = "{}) {}"
        formatted_questions = NEW_LINE.join([question_format.format(self.enumeration_chars[i], question.build())
                                             for i, question in enumerate(self.question_prompts)])
        instructions = f"{self.value}{NEW_LINE}" if self.value else ""
        return f"{instructions}{formatted_questions}"

    def __repr__(self) -> str:
        """
        Creates a representation of the questionnaire as a string
        :return: The quiestionnaire as a string
        """
        return f"{[repr(prompt) for prompt in self.question_prompts]}"
