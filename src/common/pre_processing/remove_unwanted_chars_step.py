from typing import List

from common.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep


class RemoveUnwantedCharsStep(AbstractPreProcessingStep):

    @staticmethod
    def _char2keep(char) -> bool:
        return char.isdigit() or char.isalpha()

    @staticmethod
    def _remove_unwanted_chars_from_word(word: str) -> str:
        return "".join(filter(RemoveUnwantedCharsStep._char2keep, word))

    def run(self, word_list: List[str]) -> List[str]:
        return [self._remove_unwanted_chars_from_word(word) for word in word_list]
