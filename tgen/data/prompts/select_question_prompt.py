from tgen.data.prompts.question_prompt import QuestionPrompt


class SelectQuestionPrompt(QuestionPrompt):
    """
    Asks the user to select one of a set of options.
    """

    def build(self):
        """
        Select one of the following categories:
        Category) Description
        Category) Description
        Provide the category enclosed in <category></category>.
        """
