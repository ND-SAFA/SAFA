from typing import Callable, Dict

from tgen.common.util.override import overrides
from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.data.prompts.question_prompt import QuestionPrompt


class SelectQuestionPrompt(QuestionPrompt):
    """
    Represents a Prompt that asks the model to select one of a set of options.
    """

    DEFAULT_INSTRUCTIONS = "Select one of the following categories:"
    DEFAULT_RESPONSE_FORMAT = "Enclose the category inside of {}"
    DEFAULT_RESPONSE_TAG = "category"

    def __init__(self, categories: Dict[str, str], question: str = EMPTY_STRING,
                 instructions: str = DEFAULT_INSTRUCTIONS,
                 response_format: str = DEFAULT_RESPONSE_FORMAT,
                 response_tag: str = DEFAULT_RESPONSE_TAG,
                 multiple_responses_allowed: bool = False,
                 default_factory: Callable = None):
        """
        Initializes the prompt with the categories that a model can select
        :param categories: A dictionary mapping category name to its description
        :param question: The question being asked
        :param default_factory: Method to define a default if response is not as expected
        """
        self.response_tag = response_tag
        self.instructions = instructions
        self.categories = categories
        self.response_format = response_format
        category_names = list(categories.keys())
        question = f"{question}{NEW_LINE}" if question else EMPTY_STRING
        response_manager = PromptResponseManager(response_tag=self.response_tag,
                                                 response_instructions_format=self.response_format,
                                                 expected_responses=category_names,
                                                 expected_response_type=list if multiple_responses_allowed
                                                 else type(category_names[0]),
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
