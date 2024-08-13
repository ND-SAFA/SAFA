from abc import ABC
from typing import Dict, NamedTuple, Optional

from common_resources.tools.util.json_util import JsonUtil
from common_resources.tools.util.reflection_util import ReflectionUtil


class AbstractTraceOutput(ABC):
    """
    Represents generic output from trace trainer functions.
    """

    def __init__(self, hf_output: Optional[NamedTuple]):
        """
        If defined, copies attributes of huggingface output.
        :param hf_output: The output containing same fields as instance.
        """
        if hf_output:
            ReflectionUtil.copy_attributes(hf_output, self)

    def output_to_dict(self) -> Dict:
        """
        Converts instance to a dictionary.
        :return: The output represented as a dictionary.
        """
        return JsonUtil.to_dict(self)

    def __eq__(self, other: "AbstractTraceOutput") -> bool:
        """
        Returns True if the two results are equal
        :param other: The other job result to compare
        :return: True if the two results are equal
        """
        for name, val in vars(self).items():
            if getattr(self, name) != getattr(other, name):
                return False
        return True
