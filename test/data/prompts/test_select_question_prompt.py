from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.prompts.select_question_prompt import SelectQuestionPrompt
from tgen.testres.base_tests.base_test import BaseTest


class TestSelectQuestionPrompt(BaseTest):
    CATEGORIES = {1: "Apple", 2: "Banana", 3: "Cat"}
    PROMPT = "Select one:"
    TAG = "selection"
    DEFAULT = 1

    def test_build(self):
        prompt1 = self.get_prompt()
        output1 = prompt1._build()
        self.eval_format(output1)

        prompt2 = self.get_prompt(categories=list(self.CATEGORIES.values()), numeric_category_range=range(1, 4))
        output2 = prompt2._build()
        self.assertEqual(output1, output2)
        bad_res = prompt2.parse_response("<selection>2.2</selection>")
        self.assertEqual(bad_res['selection'][0], self.DEFAULT)

        prompt3 = self.get_prompt(categories=list(self.CATEGORIES.values()), numeric_category_range=range(1, 4),
                                  categories_are_continuous=True)
        output3 = prompt3._build()
        expected_output = output1
        for i in self.CATEGORIES.keys():
            expected_output = expected_output.replace(str(i), str(float(i)))
        self.assertEqual(expected_output, output3)
        good_res = prompt3.parse_response("<selection>1.2</selection>")
        self.assertEqual(good_res['selection'][0], 1.2)

    def test_parse_response(self):
        prompt = self.get_prompt()
        response = "<selection>2</selection>"
        result = prompt.parse_response(response)
        self.assertEqual(2, result["selection"][0])

        response_bad = "<selection>5</selection>"
        result_bad = prompt.parse_response(response_bad)
        self.assertEqual(1, result_bad["selection"][0])

        prompt_multi = SelectQuestionPrompt(self.CATEGORIES, default_factory=lambda v, t: self.DEFAULT,
                                            multiple_responses_allowed=True)
        response_multi = "<categories>1,2</categories>"
        result_multi = prompt_multi.parse_response(response_multi)
        self.assertEqual([1, 2], result_multi["categories"][0])

        response_multi_bad = "<categories>1,4</categories>"
        result_multi_bad = prompt_multi.parse_response(response_multi_bad)
        self.assertEqual([1, 1], result_multi_bad["categories"][0])

    def test_correct_defaults(self):
        prompt_multi = SelectQuestionPrompt(self.CATEGORIES, multiple_responses_allowed=True)
        self.assertEqual(prompt_multi.response_tag, "categories")
        self.assertEqual(prompt_multi.response_format, "Output the categories separated by commas inside of {}")
        self.assertEqual(prompt_multi.instructions, "Select all of the categories that apply:")

        prompt_single = SelectQuestionPrompt(self.CATEGORIES, multiple_responses_allowed=False)
        self.assertEqual(prompt_single.response_tag, "category")
        self.assertEqual(prompt_single.response_format, "Enclose the category inside of {}")
        self.assertEqual(prompt_single.instructions, "Select one of the following categories:")

    def get_prompt(self, categories=CATEGORIES, allow_multiple: bool = False, **params):
        return SelectQuestionPrompt(categories, instructions=self.PROMPT,
                                    multiple_responses_allowed=allow_multiple,
                                    response_tag=self.TAG, default_factory=lambda v, t: self.DEFAULT,
                                    **params)

    def eval_format(self, output: str):
        res = output.split(NEW_LINE)
        self.assertEqual(res[0], self.PROMPT)
        categories = list(self.CATEGORIES.keys())
        self.assertTrue(res[1].startswith(f"\t{categories[0]}) {self.CATEGORIES[categories[0]]}"))
        self.assertTrue(res[2].startswith(f"\t{categories[1]}) {self.CATEGORIES[categories[1]]}"))
        self.assertTrue(res[3].startswith(f"\t{categories[2]}) {self.CATEGORIES[categories[2]]}"))
