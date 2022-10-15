import random
from copy import copy
from typing import List

from pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep, Order


class ShuffleWordsStep(AbstractPreProcessingStep):
    ORDER = Order.LAST

    def __init__(self):
        """
        Handles shuffling words
        """
        super().__init__(self.ORDER)

    def run(self, word_list: List[str]) -> List[str]:
        """
        Shuffles the words in a given word_list
        :param word_list: the list of words to shuffle
        :return: the shuffled word_list
        """
        shuffled_word_list = copy(word_list)
        random.shuffle(shuffled_word_list)
        return shuffled_word_list
