from tgen.data.prompts.prompt import Prompt


class QuestionPrompt(Prompt):
    """
    Requirements:
    - Be able to define expected response
    """

    def build(self):
        """
        QUESTION. Enclose your answer in <tag></tag>.
        """
