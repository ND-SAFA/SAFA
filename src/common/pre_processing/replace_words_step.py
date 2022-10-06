from typing import List, Dict

from common.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep, Order


class ReplaceWordsStep(AbstractPreProcessingStep):

    ORDER = Order.BEFORE

    def __init__(self, word_replace_mappings: Dict[str, str]):
        self.word_replace_mappings = word_replace_mappings
        super().__init__(self.ORDER)

    def run(self, word_list: List[str]) -> List[str]:
        for i, word in enumerate(word_list):
            if word in self.word_replace_mappings:
                word_list[i] = self.word_replace_mappings[word]
        return word_list

