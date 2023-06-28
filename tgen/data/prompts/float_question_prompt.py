from tgen.data.prompts.question_prompt import QuestionPrompt


class FloatQuestionPrompt(QuestionPrompt):
    """
    Represents a Prompt that asks the model to provide a float.
    """
    RESPONSE_FORMAT = "Return your the answer as a float inside of {}"
