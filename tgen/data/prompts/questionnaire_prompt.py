from copy import deepcopy
from string import ascii_uppercase
from typing import List, Dict, Any, Union

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.util.override import overrides


class QuestionnairePrompt(Prompt):
    """
    Contains a list of questions for the model to answer
    """

    def __init__(self, question_prompts: Union[List[QuestionPrompt], Dict[int, QuestionPrompt]], instructions: str = "",
                 response_manager: PromptResponseManager = None, enumeration_chars: List[str] = ascii_uppercase):
        """
        Initializes the questionnaire with the instructions and the questions that will make up the prompt
        :param question_prompts: The list of question prompts to include in the questionnaire
        :param instructions: Any instructions necessary with the questionnaire
        :param response_manager: Manages the responses from the prompt
        :param enumeration_chars: The list of characters to use to enumerate the questions (must include one for each question)
        """
        if isinstance(question_prompts, Dict):
            starting_number = min(question_prompts.keys())
            question_prompts = [question_prompts[i] for i in range(starting_number, len(question_prompts) + starting_number)]
        self.question_prompts = [deepcopy(prompt) for prompt in question_prompts]
        self.enumeration_chars = enumeration_chars
        self.use_bullets_for_enumeration = len(self.enumeration_chars) < len(self.question_prompts)
        if self.use_bullets_for_enumeration:
            self.enumeration_chars = [self.enumeration_chars[0] for _ in self.question_prompts]
        super().__init__(instructions, response_manager=response_manager)

    @overrides(Prompt)
    def format_value(self, *args: object, **kwargs: object) -> None:
        """
        Formats the value of all question prompts
        :param args: Args for formatting
        :param kwargs: Kwargs for formatting
        :return: None
        """
        for prompt in self.question_prompts:
            prompt.format_value(**kwargs)
        return super().format_value(*args, **kwargs)

    def parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parses the response from the model in the expected format for the prompt
        :param response: The model response
        :return: The formatted response
        """
        parsed = self.response_manager.parse_response(response)
        for prompt in self.question_prompts:
            parsed.update(prompt.response_manager.parse_response(response))
        return parsed

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
        question_format = "{}) {}" if not self.use_bullets_for_enumeration else "{} {}"
        formatted_questions = NEW_LINE.join([question_format.format(self.enumeration_chars[i], question.build())
                                             for i, question in enumerate(self.question_prompts)])
        instructions = f"{self.value}{NEW_LINE}" if self.value else ""
        return f"{instructions}{formatted_questions}{NEW_LINE}"

    def __repr__(self) -> str:
        """
        Creates a representation of the questionnaire as a string
        :return: The quiestionnaire as a string
        """
        return f"{[repr(prompt) for prompt in self.question_prompts]}"
