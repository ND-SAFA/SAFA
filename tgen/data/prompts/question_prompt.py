from tgen.data.prompts.prompt import Prompt


class QuestionPrompt(Prompt):
    """
    Represents a Prompt that asks the model a question
    """

    def __int__(self, question: str, response_tag: str = "answer"):
        """
        Initializes the prompt with the question that the model should answer
        :param question: The question the model should answer
        :param response_tag: The tags that the model should use in its response
        """
        super().__init__(value=question, response_tag=response_tag, include_expected_response=True)
