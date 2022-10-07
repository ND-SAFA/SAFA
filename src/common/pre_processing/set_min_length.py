from typing import List

from common.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep


class SetMinLength(AbstractPreProcessingStep):
    MIN_LENGTH = 1

    def run(self, word_list: List[str]) -> List[str]:
        return list(filter(lambda w: len(w.strip()) > self.MIN_LENGTH, word_list))
