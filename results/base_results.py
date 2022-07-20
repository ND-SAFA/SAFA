from abc import abstractmethod
from typing import NamedTuple


# TODO
class BaseResults():

    def __init__(self, output: NamedTuple):
        self.output = output

    @abstractmethod
    def save(self):
        pass
