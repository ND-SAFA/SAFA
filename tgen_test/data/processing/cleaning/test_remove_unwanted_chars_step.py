from common_resources.data.processing.cleaning.remove_unwanted_chars_step import RemoveUnwantedCharsStep
from tgen.testres.base_tests.base_test import BaseTest


class TestRemoveUnwantedCharStep(BaseTest):

    def test_char2keep(self):
        keep_chars = ["2", "a", "A"]
        remove_chars = ["�"]
        for char in keep_chars:
            self.assertTrue(self.get_test_step()._char2keep(char))

        for char in remove_chars:
            self.assertFalse(self.get_test_step()._char2keep(char))

    def test_remove_unwanted_chars_from_word(self):
        test_word = "test�w0rd!"
        expected_result = "testw0rd!"
        result = self.get_test_step()._remove_unwanted_chars_from_word(test_word)
        self.assertEqual(result, expected_result)

    def test_run(self):
        test_word_list = "Th!s is� a test 2 c if this method works!".split()
        expected_result = "Th!s is a test 2 c if this method works!".split()
        step = self.get_test_step()
        result = step.run(test_word_list)
        self.assertListEqual(result, expected_result)

    @staticmethod
    def get_test_step():
        return RemoveUnwantedCharsStep()
