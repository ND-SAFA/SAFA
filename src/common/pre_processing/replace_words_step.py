from typing import Dict, List

from common.pre_processing.abstract_pre_processing_step import Order, AbstractPreProcessingBeforeStep


class ReplaceWordsStep(AbstractPreProcessingBeforeStep):

    ORDER = Order.FIRST

    def __init__(self, word_replace_mappings: Dict[str, str]):
        super().__init__(self.ORDER)
        self.word_replace_mappings = word_replace_mappings

    def run(self, content: str) -> str:
        for orig_word, new_word in self.word_replace_mappings.items():
            content = content.replace(orig_word, new_word)
        return content

