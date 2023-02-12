from analysis import word_tools
from analysis.word_tools import WordCounter
from testres.base_test import BaseTest
from testres.test_assertions import TestAssertions


class TestWordCounter(BaseTest):
    SENTENCE = "a cat in a hat and a rat in a hat"
    WORD_DICT = {"a": 4, "cat": 1, "in": 2, "and": 1, "hat": 2, "rat": 1}

    def test_get_word_counts_if_meets_criteria(self):
        counter = self.get_word_counter()
        more_than_1_counter = counter.filter(lambda word, count: count > 1 and len(word) > 1)
        expected_words = ["in", "hat"]
        TestAssertions.assert_lists_have_the_same_vals(self, expected_words, more_than_1_counter.keys())
        for word in expected_words:
            self.assertEquals(self.WORD_DICT[word], more_than_1_counter[word])

    def test_from_dict(self):
        counter = WordCounter.from_dict(self.WORD_DICT)
        for word, count in self.WORD_DICT.items():
            self.assertIn(word, counter)
            self.assertEquals(counter[word], count)

    def get_word_counter(self):
        return WordCounter(self.SENTENCE.split())
