from abc import ABC
from typing import Dict, NamedTuple

from util.reflection_util import ReflectionUtil


class AbstractTraceOutput(ABC):
    """
    Represents generic output from trace trainer functions.
    """

    def __init__(self, hugging_face_instance: NamedTuple, **kwargs):
        if hugging_face_instance:
            ReflectionUtil.copy_attributes(hugging_face_instance, self)
        ReflectionUtil.set_attributes(self, kwargs)

    def output_to_dict(self) -> Dict:
        """
        Converts instance to a dictionary.
        :return: The output represented as a dictionary.
        """
        return ReflectionUtil.get_fields(self)
