from typing import List, Callable
import re
from common.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep, Order


class SeparateJoinedWordsStep(AbstractPreProcessingStep):
    ORDER = Order.FIRST

    def __init__(self):
        super().__init__(self.ORDER)

    @staticmethod
    def _separate_camel_case_word(word: str) -> List[str]:
        split_start = [0]
        for i, char in enumerate(word):
            if char.isupper() and i != 0:
                split_start.append(i)
        split_end = split_start[1:] + [len(word)]
        return [word[i:j] for i, j in zip(split_start, split_end)]

    @staticmethod
    def _separate_snake_case_word(word: str) -> List[str]:
        return word.split("_")

    @staticmethod
    def _perform_on_word_list(word_list: List[str], separator_func: Callable):
        separated_word_list = []
        for word in word_list:
            separated_word_list.extend(separator_func(word))
        return separated_word_list

    def run(self, word_list: List[str]) -> List[str]:
        separated_word_list = self._perform_on_word_list(word_list, self._separate_snake_case_word)
        return self._perform_on_word_list(separated_word_list, self._separate_camel_case_word)
