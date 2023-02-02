import json
from enum import Enum
from typing import Any, Dict, List, Union

import numpy as np

from util.reflection_util import ReflectionUtil
from util.uncased_dict import UncasedDict


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
        from util.base_object import BaseObject
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
    def read_json_file(file_path: str, as_uncased_dict: bool = False) -> Union[Dict, UncasedDict]:
        """
        Reads JSON from file at path.
        :param file_path: Path to JSON file.
        :param as_uncased_dict: Whether to convert output to uncased dict
        :return: Dictionary content of file.
        """
        with open(file_path) as file:
            content = json.load(file)
        return UncasedDict(content) if as_uncased_dict else content

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

    @staticmethod
    def read_params(source: Dict, params: List[str]) -> Dict:
        """
        Reads parameters in entry.
        :param source: The entry to extract params from
        :param params: List of params to extract.
        :return: Dictionary containing parameters from entry.
        """
        entry = {}
        for param in params:
            entry[param] = source[param]
        return entry
