from typing import Dict

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.util.override import overrides


class SelectQuestionPrompt(QuestionPrompt):
    """
    Represents a Prompt that asks the model to select one of a set of options.
    """
    QUESTION = "Select one of the following categories:"
    RESPONSE_FORMAT = "Enclose the category inside of {}"

    def __init__(self, categories: Dict[str, str]):
        """
        Initializes the prompt with the categories that a model can select
        :param categories: A dictionary mapping category name to its description
        """
        self.categories = categories
        super().__init__(self.QUESTION, response_tag="category")

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
