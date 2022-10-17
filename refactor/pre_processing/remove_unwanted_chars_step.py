from typing import List

from pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep


class RemoveUnwantedCharsStep(AbstractPreProcessingStep):

    @staticmethod
    def _char2keep(char: str) -> bool:
        """
        Determines if a char should be kept
        :param char: the char
        :return: True if char should be kept, else False
        """
        return char.isdigit() or char.isalpha()

    @staticmethod
    def _remove_unwanted_chars_from_word(word: str) -> str:
        """
        Removes unwanted chars from a word
        :param word: a word
        :returns: the word without unwanted chars
        """
        return "".join(filter(RemoveUnwantedCharsStep._char2keep, word))

    def run(self, word_list: List[str]) -> List[str]:
        """
        Removes all unwanted chars from all words in the word list
        :param word_list: the list of words to process
        :return: the processed word_list without unwanted chars
        """
        return [self._remove_unwanted_chars_from_word(word) for word in word_list]
