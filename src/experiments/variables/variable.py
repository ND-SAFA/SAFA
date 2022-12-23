from typing import Any


class Variable:

    def __init__(self, value: Any):
        """
        Base variable that holds a parameter value
        :param value: the value
        """
        self.value = value
