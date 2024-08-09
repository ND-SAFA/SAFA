from common_resources_test.base_tests.base_test import BaseTest
from common_resources.data.processing.cleaning.manual_replace_words_step import ManualReplaceWordsStep


class TestReplaceWordsStep(BaseTest):
    TEST_WORD_REPLACE_MAPPINGS = {"orig_word": "new word",
                                  "other_word": "new_word"}

    def test_run(self):
        test_content = "This is the orig_word and other_word is too."
        expected_result = "This is the new word and new_word is too."
        step = self.get_test_step()
        result = step.run(test_content.split())
        self.assertEqual(" ".join(result), expected_result)

    def get_test_step(self):
        return ManualReplaceWordsStep(self.TEST_WORD_REPLACE_MAPPINGS)
