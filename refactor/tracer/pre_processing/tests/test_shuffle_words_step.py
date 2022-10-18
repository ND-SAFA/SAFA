from test.base_test import BaseTest
from tracer.pre_processing.shuffle_words_step import ShuffleWordsStep


class TestShuffleWordsStep(BaseTest):

    def test_run(self):
        test_word_list = "This is a test".split()
        step = self.get_test_step()
        result = step.run(test_word_list)
        self.assertNotEqual(test_word_list, result)
        for word in test_word_list:
            self.assertIn(word, result)

    def get_test_step(self):
        return ShuffleWordsStep()
