from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.testres.base_tests.base_test import BaseTest


class TestQuestionnairePrompt(BaseTest):
    PROMPT = "Answer all of the following"
    STEPS = {
        1: QuestionPrompt("Think about your favorite {blank}"),
        2: QuestionPrompt("Then do this", response_manager=PromptResponseManager(response_tag="question2")),
        3: BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Do you like running?")

    }

    def test_build(self):
        questionnaire = self.get_questionnaire()
        test = questionnaire._build(blank="sport")
        self.eval_format(test)

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
                                   enumeration_chars=["i", "ii", "iii"],
                                   question_prompts=self.STEPS)

    def eval_format(self, output: str):
        res = output.split(NEW_LINE)
        self.assertEqual(res[0], self.PROMPT)
        self.assertTrue(res[1].startswith(f"i) {self.STEPS[1].value.format(blank='sport')}"))
        self.assertTrue(res[2].startswith(f"ii) {self.STEPS[2].value}"))
        self.assertTrue(res[3].startswith(f"iii) {self.STEPS[3].value}"))

