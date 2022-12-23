import enum
from abc import ABC, abstractmethod
from functools import total_ordering
from typing import List, Tuple, Iterable, Any

import math

from util.base_object import BaseObject


class ProcessingOrder(enum.Enum):
    BEFORE_WORD_SPLIT = -1
    FIRST = 0
    NEXT = 1
    ANY = 100
    LAST = math.inf


@total_ordering
class AbstractDataProcessingStep(BaseObject, ABC):
    WORD_SEP = " "

    def __init__(self, order: ProcessingOrder = ProcessingOrder.ANY):
        """
        :param order: the order the step should be run in
        """
        self.order = order

    @abstractmethod
    def run(self, data_entries: List, **kwargs) -> List:
        """
        Runs the pre-processing step on a given word_list
        :param data_entries: the list of words to process
        :return: the processed word_list
        """
        pass

    @staticmethod
    def get_word_list(content: str) -> List[str]:
        """
        Splits the content into its individual words
        :param content: the content as a string
        :return: the list of words in the content
        """
        return content.split()

    @staticmethod
    def reconstruct_content(word_list: List[str]) -> str:
        """
        Reconstructs the list of individual words into a string
        :param word_list: the list of words in the content
        :return: the content as a string
        """
        return AbstractDataProcessingStep.WORD_SEP.join(word_list)

    def __eq__(self, other):
        return self.order.value == other.order.value

    def __lt__(self, other):
        return self.order.value < other.order.value
