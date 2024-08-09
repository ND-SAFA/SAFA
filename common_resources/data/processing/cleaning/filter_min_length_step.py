from typing import List

from common_resources.tools.constants.hugging_face_constants import MIN_LENGTH_DEFAULT
from common_resources.data.processing.abstract_data_processing_step import AbstractDataProcessingStep, ProcessingOrder


class FilterMinLengthStep(AbstractDataProcessingStep):
    ORDER = ProcessingOrder.LAST
    min_length = MIN_LENGTH_DEFAULT

    def __init__(self, min_length: int = MIN_LENGTH_DEFAULT):
        """
        Handles removing all words smaller than the min_length
        :param min_length: the minimum length of word to allow
        """
        super().__init__(self.ORDER)
        self.min_length = min_length

    def run(self, word_list: List[str], **kwargs) -> List[str]:
        """
        Removes all words smaller than the min_length in a given word_list
        :param word_list: the list of words to process
        :return: the processed word_list without words smaller than min_length
        """
        return list(filter(lambda w: len(w.strip()) > self.min_length, word_list))
