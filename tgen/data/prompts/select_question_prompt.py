from typing import Callable, Dict, Any

from tgen.common.util.override import overrides
from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE, COMMA
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.data.prompts.question_prompt import QuestionPrompt


class SelectQuestionPrompt(QuestionPrompt):
    """
    Represents a Prompt that asks the model to select one of a set of options.
    """

    DEFAULT_INSTRUCTIONS = {1: "Select one of the following categories:",
                            2: "Select all of the categories that apply:"}

    DEFAULT_RESPONSE_FORMAT = {1: "Enclose the category inside of {}",
                               2: "Output the categories separated by commas inside of {}"}

    DEFAULT_RESPONSE_TAG = {1: "category",
                            2: "categories"}

    def __init__(self, categories: Dict[Any, str], question: str = EMPTY_STRING,
                 instructions: str = None,
                 response_format: str = None,
                 response_tag: str = None,
                 multiple_responses_allowed: bool = False,
                 default_factory: Callable = None):
        """
        Initializes the prompt with the categories that a model can select
        :param categories: A dictionary mapping category name to its description
        :param question: The question being asked
        :param default_factory: Method to define a default if response is not as expected
        """
        self.categories = categories
        default_key = 2 if multiple_responses_allowed else 1

        self.response_tag = response_tag if response_tag else self.DEFAULT_RESPONSE_TAG[default_key]
        self.instructions = instructions if instructions else self.DEFAULT_INSTRUCTIONS[default_key]
        self.response_format = response_format if response_format else self.DEFAULT_RESPONSE_FORMAT[default_key]
        category_names = list(self.categories.keys())
        question = f"{question}{NEW_LINE}" if question else EMPTY_STRING
        response_manager = PromptResponseManager(response_tag=self.response_tag,
                                                 response_instructions_format=self.response_format,
                                                 expected_responses=category_names,
                                                 expected_response_type=type(category_names[0]),
                                                 formatter=None if not multiple_responses_allowed else lambda t, v: v.split(COMMA),
                                                 default_factory=default_factory)
        super().__init__(f"{question}{self.instructions}",
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
        categories_format = "\t{}) {}"
        formatted_categories = NEW_LINE.join(
            [categories_format.format(category, descr) for category, descr in self.categories.items()])
        formatted_question = f"{self.value}{NEW_LINE}{formatted_categories}"
        return formatted_question
