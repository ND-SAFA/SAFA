from typing import Dict, Callable

from tgen.constants.deliminator_constants import NEW_LINE, EMPTY_STRING
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
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
        response_manager = PromptResponseManager(response_tag=self.RESPONSE_TAG, response_instructions_format=self.RESPONSE_FORMAT,
                                                 expected_responses={self.RESPONSE_TAG: category_names},
                                                 expected_response_type={self.RESPONSE_TAG: type(category_names[0])},
                                                 default_factory=default_factory)
        super().__init__(f"{question}{self.INSTRUCTIONS}",
                         response_manager=response_manager)

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
