from typing import Any, Dict, List, Union

from gen_common.constants.symbol_constants import COMMA, EMPTY_STRING, NEW_LINE
from gen_common.llm.prompts.prompt_args import PromptArgs
from gen_common.llm.prompts.question_prompt import QuestionPrompt
from gen_common.llm.response_managers.xml_response_manager import XMLResponseManager
from gen_common.util.dict_util import DictUtil
from gen_common.util.override import overrides
from gen_common.util.prompt_util import PromptUtil


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

    def __init__(self, categories: Union[List[str], Dict[Any, str]],
                 numeric_category_range: range = range(0),
                 question: str = EMPTY_STRING,
                 instructions: str = None,
                 response_format: str = None,
                 response_tag: str = None,
                 multiple_responses_allowed: bool = False,
                 categories_are_continuous: bool = False,
                 prompt_args: PromptArgs = None,
                 **response_manager_args):
        """
        Initializes the prompt with the categories that a model can select
        :param categories: A dictionary mapping category name to its description or a list of category descriptions
        :param numeric_category_range: A range from min score to max score if the category names should be scores (defaults to 0-n)
        :param question: The question being asked
        :param instructions: Additional instructions
        :param response_format: The format of the response
        :param response_tag: The tag to use for the response
        :param multiple_responses_allowed: If True, accepts multiple answers instead of a single category
        :param default_factory: Method to define a default if response is not as expected.
        :param prompt_args: The args to the base prompt.
        :param categories_are_continuous: Whether categories contain continous variables.
        """
        expected_responses = None
        if isinstance(categories, list):
            numeric_category_range = range(len(categories)) \
                if len(numeric_category_range) < len(categories) else numeric_category_range
            categories = {i: cat for i, cat in zip(numeric_category_range, categories)}
            if categories_are_continuous:
                categories = {float(i): cat for i, cat in categories.items()}
                expected_responses = numeric_category_range
        self.categories = categories
        default_key = 2 if multiple_responses_allowed else 1

        self.response_tag = response_tag if response_tag else self.DEFAULT_RESPONSE_TAG[default_key]
        self.instructions = instructions if instructions else self.DEFAULT_INSTRUCTIONS[default_key]
        self.response_format = response_format if response_format else self.DEFAULT_RESPONSE_FORMAT[default_key]
        category_names = list(self.categories.keys())
        question = f"{question}{NEW_LINE}" if question else EMPTY_STRING
        response_manager_args = DictUtil.update_kwarg_values(response_manager_args,
                                                             value_formatter=None if not multiple_responses_allowed
                                                             else lambda t, v: v.split(COMMA), replace_existing=False)
        response_manager = XMLResponseManager(response_tag=self.response_tag,
                                              response_instructions_format=self.response_format,
                                              expected_responses=category_names
                                              if expected_responses is None else expected_responses,
                                              expected_response_type=type(category_names[0]),
                                              **response_manager_args)
        super().__init__(f"{question}{self.instructions}", prompt_args=prompt_args,
                         response_manager=response_manager)

    @overrides(QuestionPrompt)
    def _build(self, **kwargs) -> str:
        """
        Formats the prompt as follows:
        Select one of the following categories:
        Category) Description
        Category) Description
        :return: The formatted prompt
        """
        if not any(self.categories.values()):
            formatted_categories = PromptUtil.format_options(list(self.categories.keys()))
        else:
            categories_format = "\n\t{}) {}"
            formatted_categories = EMPTY_STRING.join(
                [categories_format.format(category, descr) for category, descr in self.categories.items()])
        formatted_question = f"{self.value}{formatted_categories}"
        return formatted_question
