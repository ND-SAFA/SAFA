from typing import List

from data.processing.abstract_data_processing_step import AbstractDataProcessingStep, ProcessingOrder
from data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep


class RemoveUnwantedCharsStep(AbstractDataProcessingStep):
    ORDER = ProcessingOrder.FIRST
    
    def __init__(self):
        """
        Responsible for removing non alplhanumeric characters
        """
        super().__init__(order=self.ORDER)

    @staticmethod
    def _char2keep(char: str) -> bool:
        """
        Determines if a char should be kept
        :param char: the char
        :return: True if char should be kept, else False
        """
        return char.isdigit() or char.isalpha() or char in SeparateJoinedWordsStep.DELIMINATORS

    @staticmethod
    def _remove_unwanted_chars_from_word(word: str) -> str:
        """
        Removes unwanted chars from a word
        :param word: a word
        :returns: the word without unwanted chars
        """
        return "".join(filter(RemoveUnwantedCharsStep._char2keep, word))

    def run(self, word_list: List[str], **kwargs) -> List[str]:
        """
        Removes all unwanted chars from all words in the word list
        :param word_list: the list of words to process
        :return: the processed word_list without unwanted chars
        """
        return [self._remove_unwanted_chars_from_word(word) for word in word_list]
