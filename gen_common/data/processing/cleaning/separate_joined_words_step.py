from typing import Callable, Iterable, List

from gen_common.constants.symbol_constants import UNDERSCORE
from gen_common.data.processing.abstract_data_processing_step import AbstractDataProcessingStep, ProcessingOrder


class SeparateJoinedWordsStep(AbstractDataProcessingStep):
    ORDER = ProcessingOrder.FIRST
    DELIMINATORS = (UNDERSCORE, "/")

    def __init__(self, deliminators: Iterable[str] = DELIMINATORS):
        """
        Handles separating all camelCase and snake_case words
        :param deliminators: Deliminators used to split words.
        """
        self.deliminators = deliminators
        super().__init__(self.ORDER)

    @staticmethod
    def separate_camel_case_word(word: str) -> List[str]:
        """
        Splits a camelCase word
        :param word: the word to split
        :return: the split up word
        """
        split_start = [0]
        for i, char in enumerate(word):
            if char.isupper() and i != 0:
                split_start.append(i)
        split_end = split_start[1:] + [len(word)]
        return [word[i:j] for i, j in zip(split_start, split_end)]

    @staticmethod
    def separate_deliminated_word(word: str, deliminator: str = UNDERSCORE) -> List[str]:
        """
        Splits a deliminated word (e.g. snake_case)
        :param word: the word to split
        :param deliminator: The deliminator used to join the words
        :return: the split up word
        """
        return word.split(deliminator)

    @staticmethod
    def _perform_on_word_list(word_list: List[str], separator_func: Callable):
        """
        Performs separation task on the word list
        :param word_list: the list of words to separate
        :param separator_func: The function transforming single word in to many.
        :return: the separated word_list
        """
        separated_word_list = []
        for word in word_list:
            separated_word_list.extend(separator_func(word))
        return separated_word_list

    def run(self, word_list: List[str], **kwargs) -> List[str]:
        """
        Separates all camelCase and snake_case words on a given word_list
        :param word_list: the list of words to process
        :return: the processed word_list with camelCase and snake_case separated
        """
        separated_word_list = word_list
        for deliminator in self.deliminators:
            separated_word_list = self._perform_on_word_list(separated_word_list,
                                                             lambda word: self.separate_deliminated_word(word, deliminator))
        return self._perform_on_word_list(separated_word_list, self.separate_camel_case_word)
