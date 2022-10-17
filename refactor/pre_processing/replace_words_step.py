from typing import Dict

from pre_processing.abstract_pre_processing_step import AbstractPreProcessingBeforeStep, Order


class ReplaceWordsStep(AbstractPreProcessingBeforeStep):
    ORDER = Order.FIRST

    def __init__(self, word_replace_mappings: Dict[str, str]):
        """
        Handles replacing all words in the word_replace_mappings
        :param word_replace_mappings
        """
        super().__init__(self.ORDER)
        self.word_replace_mappings = word_replace_mappings

    def run(self, content: str) -> str:
        """
        Replaces words from word_replace_mappings on a given content string
        :param content: the content string to process
        :return: the processed string with word replacements
        """
        for orig_word, new_word in self.word_replace_mappings.items():
            content = content.replace(orig_word, new_word)
        return content
