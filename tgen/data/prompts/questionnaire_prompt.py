from typing import List

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.question_prompt import QuestionPrompt


class QuestionnairePrompt(Prompt):
    """
    Contains a list of questions
    """

    def __init__(self, question_prompts: List[QuestionPrompt], value: str):
        super().__init__(value)
        self.question_prompts = question_prompts

    def build(self, question_prompts: List[QuestionPrompt]):
        """
        A) Question 1
        B) ...
        C) Question n
        """
