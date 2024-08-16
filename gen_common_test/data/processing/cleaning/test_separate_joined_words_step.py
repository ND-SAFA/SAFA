from gen_common.constants import UNDERSCORE
from gen_common_test.base_tests.base_test import BaseTest
from gen_common.data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep


class TestSeparateJoinedWordsStep(BaseTest):
    TEST_DELIMINATORS = ("_", "/")

    def test_separate_camel_case_word(self):
        test_camel_case = "camelCase2"
        expected_result = ["camel", "Case2"]
        result = SeparateJoinedWordsStep.separate_camel_case_word(test_camel_case)
        self.assertListEqual(result, expected_result)
        test_regular_word = "Regular"
        result = SeparateJoinedWordsStep.separate_camel_case_word(test_regular_word)
        self.assertListEqual(result, [test_regular_word])

    def test_separate_deliminated_word(self):
        test_camel_case = "snake_case"
        expected_result = ["snake", "case"]
        result = SeparateJoinedWordsStep.separate_deliminated_word(test_camel_case, deliminator=UNDERSCORE)
        self.assertListEqual(result, expected_result)
        test_regular_word = "Regular"
        result = SeparateJoinedWordsStep.separate_deliminated_word(test_regular_word)
        self.assertListEqual(result, [test_regular_word])

    def test_run(self):
        test_word_list = "This is an example of a camelCase Word. This is snake_case. This is another example/sample/examplar".split()
        expected_result = "This is an example of a camel Case Word. This is snake case. This is another example sample examplar".split()
        step = self.get_test_step()
        result = step.run(test_word_list)
        self.assertListEqual(expected_result, result)

    def get_test_step(self):
        return SeparateJoinedWordsStep(self.TEST_DELIMINATORS)
