import enum
from abc import ABC, abstractmethod
from functools import total_ordering
from typing import List, Tuple

import math


class Order(enum.Enum):
    FIRST = 0
    ANY = 100
    LAST = math.inf


@total_ordering
class AbstractPreProcessingStep(ABC):

    def __init__(self, order: Order = Order.ANY, run_before: bool = False):
        """
        :param order: the order the step should be run in
        :param run_before: if True, the step will be run before splitting the content into a word list
        """
        self.order = order
        self.run_before = run_before

    @abstractmethod
    def run(self, word_list: List[str]) -> List[str]:
        """
        Runs the pre-processing step on a given word_list
        :param word_list: the list of words to process
        :return: the processed word_list
        """
        pass

    def __eq__(self, other):
        return self.order.value == other.order.value

    def __lt__(self, other):
        return self.order.value < other.order.value


class AbstractPreProcessingBeforeStep(AbstractPreProcessingStep, ABC):

    def __init__(self, order: Order = Order.ANY):
        """
        :param order: the order the step should be run in
        """
        super().__init__(order, run_before=True)

    @abstractmethod
    def run(self, content: str) -> str:
        """
        Runs the pre-processing step on a given content string
        :param content: the content string to process
        :return: the processed string
        """
        pass


class AbstractPreProcessingLinkStep(AbstractPreProcessingStep, ABC):

    @abstractmethod
    def run(self, true_links: List[Tuple[str, str]], **kwargs) -> str:
        """
        Runs the pre-processing step on a given content string
        :param content: the content string to process
        :return: the processed string
        """
        pass