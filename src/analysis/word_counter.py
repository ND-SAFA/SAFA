from collections import Counter
from typing import Iterable, Dict, Callable


class WordCounter(Counter):

    def __init__(self, words: Iterable[str] = None):
        super().__init__(words)
        self.total = sum(self.values())

    @staticmethod
    def from_dict(word_counts: Dict[str, int]) -> "WordCounter":
        """
        Creates a counter from a dictionary mapping words to their counts
        :param word_counts: A dictionary mapping words to their counts
        :return: The counter
        """
        return WordCounter(word_counts)

    def filter(self, criteria: Callable) -> "WordCounter":
        """
        Gets all words and their count if the count meets the criteria
        :param criteria: A callable that returns True if criteria is met
        :return: A dictionary of words and their count if the count meets the criteria
        """
        return WordCounter.from_dict({word: count for word, count in self.items() if criteria(word, count)})
