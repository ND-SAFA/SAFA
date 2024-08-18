from gen_common.llm.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from gen_common_test.base.tests.base_test import BaseTest


class TestBinaryChoiceQuestionPrompt(BaseTest):
    CHOICES = ["yes", "no"]
    PROMPT = "Choice one: "
    DEFAULT = "yes"
    TAG = "tag"

    def test_build(self):
        prompt = self.get_prompt()
        output = prompt.build()
        self.assertTrue(output.startswith(self.PROMPT))
        self.assertTrue(output.endswith(f"<{self.TAG}></{self.TAG}>"))
        self.assertIn(BinaryChoiceQuestionPrompt.RESPONSE_INSTRUCTIONS1.format(*self.CHOICES), output)

    def test_parse_response(self):
        prompt = self.get_prompt()
        self.assertEqual("no", prompt.parse_response("<tag>no</tag>")[self.TAG][0])
        self.assertEqual("yes", prompt.parse_response("<tag>nope</tag>")[self.TAG][0])

    def get_prompt(self):
        return BinaryChoiceQuestionPrompt(self.CHOICES, self.PROMPT, response_tag=self.TAG,
                                          default_factory=lambda t, v: self.DEFAULT)
