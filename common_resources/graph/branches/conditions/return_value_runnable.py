from copy import deepcopy
from typing import Any

from langchain_core.runnables.base import RunnableLambda


class ReturnValueRunnable(RunnableLambda):

    def __init__(self, value: Any):
        """
        Makes a string appear to be a runnable.
        :param value: String value.
        """
        super().__init__(lambda x, val=value: deepcopy(val))
