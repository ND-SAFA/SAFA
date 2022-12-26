from typing import Any


class Variable:

    def __init__(self, value: Any):
        """
        Base variable that holds a parameter value
        :param value: the value
        """
        self.value = value

    def __repr__(self) -> str:
        """
        Returns a string representation
        :return: a string representation
        """
        return "%s(%s)" % (self.__class__.__name__, str(self.value))
