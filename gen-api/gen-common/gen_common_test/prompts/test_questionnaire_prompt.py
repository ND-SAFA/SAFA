from gen_common.constants.symbol_constants import NEW_LINE
from gen_common.llm.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from gen_common.llm.prompts.question_prompt import QuestionPrompt
from gen_common.llm.prompts.questionnaire_prompt import QuestionnairePrompt
from gen_common.llm.response_managers.xml_response_manager import XMLResponseManager
from gen_common.util.prompt_util import PromptUtil
from gen_common_test.base.tests.base_test import BaseTest


class TestQuestionnairePrompt(BaseTest):
    PROMPT = "Answer all of the following"
    STEPS = {
        1: QuestionPrompt("Think about your favorite {blank}"),
        2: QuestionPrompt("Then do this", response_manager=XMLResponseManager(response_tag="question2")),
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

    def test_get_prompt_by_primary_tag(self):
        questionnaire = self.get_questionnaire()
        prompt = questionnaire.get_prompt_by_primary_tag("question2")
        self.assertEqual(questionnaire.child_prompts[1].args.prompt_id, prompt.args.prompt_id)
        questionnaire = self.get_questionnaire()
        prompt = questionnaire.get_prompt_by_primary_tag("unknown")
        self.assertIsNone(prompt)

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
        self.assertTrue(res[5].startswith(PromptUtil.indent_for_markdown(f"- {self.STEPS[4].child_prompts[0]}")))
