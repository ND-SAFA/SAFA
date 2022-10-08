import enum
from abc import ABC, abstractmethod
from functools import total_ordering
from typing import List

import math


class Order(enum.Enum):
    FIRST = 0
    ANY = 100
    LAST = math.inf


@total_ordering
class AbstractPreProcessingStep(ABC):

    def __init__(self, order: Order = Order.ANY, run_before: bool = False):
        self.order = order
        self.run_before = run_before

    @abstractmethod
    def run(self, word_list: List[str]) -> List[str]:
        pass

    def __eq__(self, other):
        return self.order.value == other.order.value

    def __lt__(self, other):
        return self.order.value < other.order.value


class AbstractPreProcessingBeforeStep(AbstractPreProcessingStep, ABC):

    def __init__(self, order: Order = Order.ANY):
        super().__init__(order, True)

    @abstractmethod
    def run(self, content: str) -> str:
        pass
