from gen_common_test.base_tests.base_test import BaseTest
from gen_common.data.processing.cleaning.remove_white_space_step import RemoveWhiteSpaceStep


class TestRemoveWhitespaceStep(BaseTest):

    def test_run(self):
        test_word_list = "  This sentence has    a lot    of extra whitespace     ".split()
        expected_result = "This sentence has a lot of extra whitespace".split()
        step = self.get_test_step()
        result = step.run(test_word_list)
        self.assertEqual(expected_result, result)

    def get_test_step(self):
        return RemoveWhiteSpaceStep()
