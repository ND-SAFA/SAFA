from typing import List

from tracer.pre_processing.steps.abstract_pre_processing_step import AbstractPreProcessingStep


class RemoveWhiteSpaceStep(AbstractPreProcessingStep):

    def run(self, word_list: List[str]) -> List[str]:
        stripped_word_list = []
        for word in word_list:
            stripped_word_list.append(word.strip())
        return stripped_word_list
