from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from tgen.prompts.prompt_response_manager import PromptResponseManager
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.testres.base_tests.base_test import BaseTest


class TestQuestionnairePrompt(BaseTest):
    PROMPT = "Answer all of the following"
    STEPS = {
        1: QuestionPrompt("Think about your favorite {blank}"),
        2: QuestionPrompt("Then do this", response_manager=PromptResponseManager(response_tag="question2")),
        3: BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Do you like running?"),
        4: QuestionnairePrompt(instructions="Then answer these {blank2}",
                               question_prompts=[QuestionPrompt("This is another question!")], enumeration_chars=["-"])

    }

    def test_build(self):
        questionnaire = self.get_questionnaire()
        test = questionnaire._build(blank="sport", blank2="questions")
        self.eval_format(test)

        questionnaire.enumeration_chars = ["1", "2"]
        test_with_not_enough_enumeration = questionnaire._build(blank="sport", blank2="questions")
        res = test_with_not_enough_enumeration.split(NEW_LINE)
        self.assertTrue(res[3].startswith(f"1) {self.STEPS[3].value}"))

    def test_parse_response(self):
        questionnaire = self.get_questionnaire()
        response = "<question2>Okay</question2><choice>no</choice>"
        result = questionnaire.parse_response(response)
        self.assertIn("question2", result)
        self.assertEqual(result["question2"][0], "Okay")
        self.assertIn("choice", result)
        self.assertEqual(result["choice"][0], "no")

    def get_questionnaire(self):
        return QuestionnairePrompt(instructions="Answer all of the following",
                                   enumeration_chars=["i", "ii", "iii", "iv"],
                                   question_prompts=self.STEPS)

    def eval_format(self, output: str):
        res = output.split(NEW_LINE)
        self.assertEqual(res[0], self.PROMPT)
        self.assertTrue(res[1].startswith(f"i) {self.STEPS[1].value.format(blank='sport')}"))
        self.assertTrue(res[2].startswith(f"ii) {self.STEPS[2].value}"))
        self.assertTrue(res[3].startswith(f"iii) {self.STEPS[3].value}"))
        self.assertTrue(res[4].startswith(f"iv) {self.STEPS[4].value.format(blank2='questions')}"))
        self.assertTrue(res[5].startswith(PromptUtil.indent_for_markdown(f"- {self.STEPS[4].question_prompts[0]}")))

