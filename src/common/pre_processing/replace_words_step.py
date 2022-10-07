from typing import Dict, List

from common.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep, Order


class ReplaceWordsStep(AbstractPreProcessingStep):
    ORDER = Order.BEFORE

    def __init__(self, word_replace_mappings: Dict[str, str]):
        self.word_replace_mappings = word_replace_mappings
        super().__init__(self.ORDER)

    def run(self, word_list: List[str]) -> List[str]:
        new_word_list = []
        for word in word_list:
            if word in self.word_replace_mappings:
                new_word_list.extend(self.word_replace_mappings[word].split())
            else:
                new_word_list.append(word)
        return new_word_list
