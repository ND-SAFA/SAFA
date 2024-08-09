import random

from common_resources.data.processing.cleaning.shuffle_words_step import ShuffleWordsStep
from common_resources_test.base_tests.base_test import BaseTest


class TestShuffleWordsStep(BaseTest):

    def test_run(self):
        random.seed(0)
        test_word_list = "This is a test".split()
        step = self.get_test_step()
        result = step.run(test_word_list)
        self.assertNotEqual(test_word_list, result)
        for word in test_word_list:
            self.assertIn(word, result)

    def get_test_step(self):
        return ShuffleWordsStep()
