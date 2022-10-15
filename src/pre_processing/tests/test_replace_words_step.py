from pre_processing.replace_words_step import ReplaceWordsStep
from test.base_test import BaseTest


class TestReplaceWordsStep(BaseTest):
    TEST_WORD_REPLACE_MAPPINGS = {"orig_word": "new word",
                                  "orig word": "new_word"}

    def test_run(self):
        test_content = "This is the orig_word and orig word is too."
        expected_result = "This is the new word and new_word is too."
        step = self.get_test_step()
        result = step.run(test_content)
        self.assertEquals(result, expected_result)

    def get_test_step(self):
        return ReplaceWordsStep(self.TEST_WORD_REPLACE_MAPPINGS)
