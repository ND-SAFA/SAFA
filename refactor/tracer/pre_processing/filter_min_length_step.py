from typing import List

from tracer.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep, Order


class FilterMinLengthStep(AbstractPreProcessingStep):
    ORDER = Order.LAST

    def __init__(self, min_length: int = 1):
        """
        Handles removing all words smaller than the min_length
        min_length: the minimum length of word to allow
        """
        super().__init__(self.ORDER)
        self.min_length = min_length

    def run(self, word_list: List[str]) -> List[str]:
        """
        Removes all words smaller than the min_length in a given word_list
        :param word_list: the list of words to process
        :return: the processed word_list without words smaller than min_length
        """
        return list(filter(lambda w: len(w.strip()) > self.min_length, word_list))
