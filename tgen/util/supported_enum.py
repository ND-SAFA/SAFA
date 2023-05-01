from enum import Enum
from typing import Any, List, Type

from tgen.util.reflection_util import ReflectionUtil


class SupportedEnum(Enum):
    """
    Contains utility methods for retrieving enum values.
    """

    @classmethod
    def get_value(cls, key_name: str) -> Any:
        """
        Returns the enum value whose key matches given name.
        :param key_name: Case-insensitive key name.
        :return: Enum value.
        """
        key_name = key_name.upper()
        for k in cls._value2member_map_.values():
            if k.name == key_name:
                return k.value
        raise ValueError(f"{key_name} is not one of {cls.get_keys()}")

    @classmethod
    def has_key(cls, key_name: str) -> bool:
        """
        :param key_name: The key interested in check for associated value.
        :return:Returns is value under key name.
        """
        try:
            cls.get_value(key_name)
            return True
        except:
            return False

    @classmethod
    def has_value(cls, value: object):
        """
        Returns true if value if one of the value of a key.
        :param value: The value to check existence for.
        :return: Whether value is contained within enum.
        """
        for k in cls._value2member_map_.keys():
            if value == k or ReflectionUtil.is_instance_or_subclass(value, k):
                return True
        return False

    @classmethod
    def get_keys(cls) -> List[str]:
        """
        :return: Returns list of keys in enum.
        """
        return [k.name for k in cls._value2member_map_.values()]

    @classmethod
    def get_values(cls):
        """
        :return: Returns the values of the supported enums.
        """
        return [v for v in cls._value2member_map_.keys()]

    @classmethod
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: self, the enum class mapping name to class
        """
        return cls
