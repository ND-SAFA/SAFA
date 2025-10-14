from gen_common.llm.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from gen_common.llm.response_managers.json_response_manager import JSONResponseManager


class BinaryScorePrompt(BinaryChoiceQuestionPrompt):
    """
    Represents a Prompt that asks the model to select one of yes or no.
    """
    YES = "yes"
    NO = "no"
    RESPONSE_TAG = "binary_score"

    def __init__(self,  question: str, yes_descr: str, no_descr: str = "otherwise",
                 response_descr: str = "Respond with only", **kwargs):
        """
        Initializes the prompt with the categories that a model can select
        :param question: The question being asked.
        :param yes_descr: Description of what yes means.
        :param no_descr: Description of what no means.
        :param response_descr: Description of expected response.
        """
        choices = {BinaryScorePrompt.YES: yes_descr,
                   BinaryScorePrompt.NO: no_descr}
        tag_descriptions = {BinaryScorePrompt.RESPONSE_TAG: f"{response_descr}, {BinaryScorePrompt.YES} or {BinaryScorePrompt.NO}"}
        response_tag = BinaryScorePrompt.RESPONSE_TAG
        super().__init__(choices=choices, question=question, tag_descriptions=tag_descriptions, response_tag=response_tag,
                         response_manager_type=JSONResponseManager, **kwargs)
