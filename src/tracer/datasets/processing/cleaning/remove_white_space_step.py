from typing import List

from tracer.datasets.processing.abstract_data_processing_step import AbstractDataProcessingStep, ProcessingOrder


class RemoveWhiteSpaceStep(AbstractDataProcessingStep):
    ORDER = ProcessingOrder.FIRST

    def __init__(self):
        """
        Responsible for removing white space
        """
        super().__init__(order=self.ORDER)

    def run(self, word_list: List[str], **kwargs) -> List[str]:
        stripped_word_list = []
        for word in word_list:
            stripped_word_list.append(word.strip())
        return stripped_word_list
