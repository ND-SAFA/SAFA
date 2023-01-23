from abc import ABC
from typing import Dict, NamedTuple, Optional

from util.reflection_util import ReflectionUtil


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
        return ReflectionUtil.jsonify(self)
