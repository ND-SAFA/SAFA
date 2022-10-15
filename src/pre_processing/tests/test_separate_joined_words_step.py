from pre_processing.separate_joined_words_step import SeparateJoinedWordsStep
from test.base_test import BaseTest


class TestSeparateJoinedWordsStep(BaseTest):

    def test_separate_camel_case_word(self):
        test_camel_case = "camelCase2"
        expected_result = ["camel", "Case2"]
        result = SeparateJoinedWordsStep._separate_camel_case_word(test_camel_case)
        self.assertListEqual(result, expected_result)
        test_regular_word = "Regular"
        result = SeparateJoinedWordsStep._separate_camel_case_word(test_regular_word)
        self.assertListEqual(result, [test_regular_word])

    def test_separate_snake_case_word(self):
        test_camel_case = "snake_case"
        expected_result = ["snake", "case"]
        result = SeparateJoinedWordsStep._separate_snake_case_word(test_camel_case)
        self.assertListEqual(result, expected_result)
        test_regular_word = "Regular"
        result = SeparateJoinedWordsStep._separate_snake_case_word(test_regular_word)
        self.assertListEqual(result, [test_regular_word])

    def test_run(self):
        test_word_list = "This is an example of a camelCase Word.".split()
        expected_result = "This is an example of a camel Case Word.".split()
        step = self.get_test_step()
        result = step.run(test_word_list)
        self.assertEquals(expected_result, result)

    def get_test_step(self):
        return SeparateJoinedWordsStep()
