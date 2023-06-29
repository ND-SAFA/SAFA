from enum import StrEnum, auto
from typing import Dict, Callable

from tgen.constants.deliminator_constants import NEW_LINE, EMPTY_STRING, SPACE
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.util.override import overrides


class SelectQuestionPrompt(QuestionPrompt):
    """
    Represents a Prompt that asks the model to select one of a set of options.
    """

    INSTRUCTIONS = "Select one of the following categories:"
    RESPONSE_FORMAT = "Enclose the category inside of {}"
    RESPONSE_TAG = "category"

    def __init__(self, categories: Dict[str, str], question: str = EMPTY_STRING, default_factory: Callable = None):
        """
        Initializes the prompt with the categories that a model can select
        :param categories: A dictionary mapping category name to its description
        :param question: The question being asked
        :param default_factory: Method to define a default if response is not as expected
        """
        self.categories = categories
        category_names = list(categories.keys())
        question = f"{question}{NEW_LINE}" if question else EMPTY_STRING
        super().__init__(f"{question}{self.INSTRUCTIONS}",
                         response_tag=self.RESPONSE_TAG,
                         expected_responses=category_names, response_instructions=self.RESPONSE_FORMAT,
                         expected_response_type=type(category_names[0]), default_factory=default_factory)

    @overrides(QuestionPrompt)
    def _build(self) -> str:
        """
        Formats the prompt as follows:
        Select one of the following categories:
        Category) Description
        Category) Description
        :return: The formatted prompt
        """
        categories_format = "{}) {}"
        formatted_categories = NEW_LINE.join([categories_format.format(category, descr) for category, descr in self.categories])
        formatted_question = f"{self.value}{NEW_LINE}{formatted_categories}"
        return formatted_question
