from enum import Enum
from typing import Any, List

from gen_common.util.reflection_util import ReflectionUtil


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
        try:
            return SupportedEnum[key_name].value
        except KeyError:
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
        except Exception:
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

    def to_yaml(self, export_path: str = None) -> str:
        """
        Converts enum to name so it can be read from yaml
        :param export_path: The path to store yamified value to.
        :return: The name of the enum
        """
        if export_path:
            return self
        return self.name

    @classmethod
    def from_yaml(cls, val: str) -> "SupportedEnum":
        """
        Converts enum name to the correct supported enum after being read from yaml.
        :param val: The yaml value to read into supported enum.
        :return: The supported enum obj
        """
        return cls[val]

    def __iter__(self):
        """
        Iterates through each enum.
        :return: Next enum.
        """
        for enum_key in self.get_keys():
            yield self[enum_key]

    def __deepcopy__(self, memodict={}) -> "SupportedEnum":
        """
        Makes a copy of the enum bc Python struggles for some reason
        :param memodict: Unused
        :return: A copy of the Enum
        """
        return self.__class__[self.name]
