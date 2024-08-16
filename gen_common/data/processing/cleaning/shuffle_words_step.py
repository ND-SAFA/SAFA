import random
from copy import copy
from typing import List

from gen_common.data.processing.abstract_data_processing_step import AbstractDataProcessingStep, ProcessingOrder


class ShuffleWordsStep(AbstractDataProcessingStep):
    ORDER = ProcessingOrder.LAST

    def __init__(self):
        """
        Handles shuffling words
        """
        super().__init__(self.ORDER)

    def run(self, word_list: List[str], **kwargs) -> List[str]:
        """
        Shuffles the words in a given word_list
        :param word_list: the list of words to shuffle
        :return: the shuffled word_list
        """
        shuffled_word_list = copy(word_list)
        random.shuffle(shuffled_word_list)
        return shuffled_word_list
