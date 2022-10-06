import enum
from abc import abstractmethod, ABC
from enum import IntEnum
from functools import total_ordering
from typing import List


@total_ordering
class Order(IntEnum):
    FIRST = enum.auto()
    ANY = enum.auto()
    LAST = enum.auto()

    def __lt__(self, other):
        if other == Order.FIRST or self == Order.LAST:
            return False
        return True


@total_ordering
class AbstractPreProcessingStep(ABC):

    def __init__(self, order: Order = Order.ANY):
        self.order = order

    @abstractmethod
    def run(self, word_list: List[str]) -> List[str]:
        pass

    def __eq__(self, other):
        return self.order == other.order

    def __lt__(self, other):
        return self.order < other.order
