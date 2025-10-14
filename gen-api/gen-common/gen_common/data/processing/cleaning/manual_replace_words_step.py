from typing import Dict, List

from gen_common.data.processing.abstract_data_processing_step import AbstractDataProcessingStep, ProcessingOrder
from gen_common.util.uncased_dict import UncasedDict


class ManualReplaceWordsStep(AbstractDataProcessingStep):
    """
    Performs replacements based on word matchings.
    """
    ORDER = ProcessingOrder.NEXT
    word_replace_mappings = None

    def __init__(self, word_replace_mappings: Dict[str, str]):
        """
        Handles replacing all words in the word_replace_mappings
        :param word_replace_mappings
        """
        super().__init__(self.ORDER)
        self.word_replace_mappings = UncasedDict(word_replace_mappings)

    def run(self, word_list: List[str], **kwargs) -> List[str]:
        """
        Replaces words from word_replace_mappings on a given word list
        :param word_list: the list of words to separate
        :return: the processed word list with word replacements
        """
        new_word_list = []
        for word in word_list:
            replacement = self.word_replace_mappings[word] if word in self.word_replace_mappings else word
            new_word_list.append(replacement)
        return new_word_list
