from random import random
from typing import List

from common.pre_processing.abstract_pre_processing_step import AbstractPreProcessingStep


class ShuffleWordsStep(AbstractPreProcessingStep):

    def run(self, word_list: List[str]) -> List[str]:
        return random.shuffle(word_list)
