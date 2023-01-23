import json
from enum import Enum
from typing import Any, Dict, List

import numpy as np

from util.base_object import BaseObject
from util.reflection_util import ReflectionUtil


class NpEncoder(json.JSONEncoder):
    """
    Handles Numpy conversion to json
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if hasattr(obj, "_fields"):
            instance_fields: Dict = ReflectionUtil.get_fields(obj)
            return self.default(instance_fields)
        if isinstance(obj, Enum):
            return obj.name
        if isinstance(obj, BaseObject):
            return str(obj)
        if isinstance(obj, list):
            return [self.default(v) for v in obj]
        if hasattr(obj, "__dict__"):
            instance_fields: Dict = ReflectionUtil.get_fields(obj)
            return {k: self.default(v) for k, v in instance_fields.items()}
        return obj


class JsonUtil:
    """
    Provides utility methods for dealing with JSON / Dict.
    """

    @staticmethod
    def dict_to_json(dict_: Dict) -> str:
        """
        Converts the dictionary to json
        :param dict_: the dictionary
        :return: the dictionary as json
        """
        return json.dumps(dict_, indent=4, cls=NpEncoder)

    @staticmethod
    def require_properties(json_obj: Dict, required_properties: List[str]) -> None:
        """
        Verifies that the json object contains each property. Throws error otherwise.
        :param json_obj: The json object to verify.
        :param required_properties: List of properties to verify exist in json object.
        :return: None
        """
        for required_property in required_properties:
            if required_property not in json_obj:
                raise Exception(f"Expected {required_property} in: \n{json.dumps(json_obj, indent=4)}.")

    @staticmethod
    def get_property(definition: Dict, property_name: str, default_value=None) -> Any:
        """
        Returns property in definition if exists. Otherwise, default is returned is available.
        :param definition: The base dictionary to retrieve property from.
        :param property_name: The name of the property to retrieve.
        :param default_value: The default value to return if property is not found.
        :return: The property under given name.
        """
        if property_name not in definition and default_value is None:
            raise ValueError(definition, "does not contain property: ", property_name)
        return definition.get(property_name, default_value)

    @staticmethod
    def to_dict(instance: Any) -> Dict:
        """
        Converts object to serialize dictionary.
        :param instance: The instance to convert to dictionary.
        :return: The serializable dictionary.
        """
        encoder = NpEncoder()
        return encoder.default(instance)
