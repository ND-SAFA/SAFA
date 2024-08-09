import string
from typing import Dict, List, Union

from common_resources.data.processing.abstract_data_processing_step import AbstractDataProcessingStep, ProcessingOrder
from common_resources.data.processing.cleaning.manual_replace_words_step import ManualReplaceWordsStep


class RemoveUnwantedCharsStep(AbstractDataProcessingStep):
    ORDER = ProcessingOrder.FIRST

    def __init__(self, additional_unwanted_chars: Union[Dict[str, str], List[str]] = None):
        """
        Responsible for any non-printable or additional unwanted characters.
        :param additional_unwanted_chars: Other unwanted character to remove.
        """
        if isinstance(additional_unwanted_chars, list):
            additional_unwanted_chars = {c: "" for c in additional_unwanted_chars}
        self.additional_unwanted_chars = {} if additional_unwanted_chars is None else additional_unwanted_chars
        self.replace_step = ManualReplaceWordsStep(word_replace_mappings=self.additional_unwanted_chars)
        super().__init__(order=self.ORDER)

    def _char2keep(self, char: str) -> bool:
        """
        Determines if a char should be kept
        :param char: the char
        :return: True if char should be kept, else False
        """
        return char in string.printable  # and char not in self.additional_unwanted_chars

    def _remove_unwanted_chars_from_word(self, word: str) -> str:
        """
        Removes unwanted chars from a word
        :param word: a word
        :returns: the word without unwanted chars
        """
        word = "".join(self.replace_step.run(list(word)))
        return "".join(filter(self._char2keep, word))

    def run(self, word_list: List[str], **kwargs) -> List[str]:
        """
        Removes all unwanted chars from all words in the word list
        :param word_list: the list of words to process
        :return: the processed word_list without unwanted chars
        """
        return [self._remove_unwanted_chars_from_word(word) for word in word_list]
