from typing import List, Callable
import re
from common.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep, Order


class SeparateJoinedWordsStep(AbstractPreProcessingStep):
    ORDER = Order.FIRST

    def __init__(self):
        super().__init__(self.ORDER)

    @staticmethod
    def _capitalize_first_letter(word: str) -> str:
        first_letter = word[0].upper()
        return first_letter + word[1:] if len(word) > 1 else first_letter

    @staticmethod
    def _separate_camel_case_word(word: str) -> List[str]:
        word = SeparateJoinedWordsStep._capitalize_first_letter(word)
        separated_words = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', word)
        return separated_words

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
