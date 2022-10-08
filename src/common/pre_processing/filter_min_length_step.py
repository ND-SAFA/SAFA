from typing import List

from common.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep, Order


class FilterMinLengthStep(AbstractPreProcessingStep):
    ORDER = Order.LAST

    def __init__(self, min_length: int = 1):
        super().__init__(self.ORDER)
        self.min_length = min_length

    def run(self, word_list: List[str]) -> List[str]:
        return list(filter(lambda w: len(w.strip()) > self.min_length, word_list))
