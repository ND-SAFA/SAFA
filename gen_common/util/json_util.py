import json
import uuid
from enum import Enum
from typing import Any, Dict, List, Union

import numpy as np

from gen_common.util.reflection_util import ReflectionUtil
from gen_common.util.uncased_dict import UncasedDict


class NpEncoder(json.JSONEncoder):
    """
    Handles Numpy conversion to json
    """

    def default(self, obj: Any):
        """
        Encodes object into JSON.
        :param obj: The object to encode.
        :return: The dictionary representing that object.
        """
        from gen_common.data.tdatasets.trace_dataset import TraceDataset
        if isinstance(obj, TraceDataset):
            from gen_common.data.exporters.api_exporter import ApiExporter
            api_definition = ApiExporter(dataset=obj).export()
            return self.default(api_definition)
        from transformers.training_args import TrainingArguments
        if isinstance(obj, TrainingArguments):
            obj_vars = {k: self.default(v) for k, v in vars(obj.__class__).items() if not k.startswith("_")}
            return obj_vars
        from gen_common.util.base_object import BaseObject
        if isinstance(obj, BaseObject):
            obj_fields = ReflectionUtil.get_fields(obj)
            new_fields = {}
            for field_name, field_value in obj_fields.items():
                new_fields[field_name] = self.default(field_value)
            return new_fields
        if isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, set):
            return list(obj)
        elif hasattr(obj, "_fields"):
            instance_fields: Dict = ReflectionUtil.get_fields(obj)
            return self.default(instance_fields)
        elif isinstance(obj, Enum):
            return obj.name
        elif isinstance(obj, list) or isinstance(obj, tuple):
            return [self.default(v) for v in obj]
        elif isinstance(obj, dict):
            value = {self.default(k): self.default(v) for k, v in obj.items()}
            return value
        elif hasattr(obj, "__dict__") and not isinstance(obj, str):
            instance_fields: Dict = ReflectionUtil.get_fields(obj)
            new_dict = {}
            for k, v in instance_fields.items():
                new_dict[self.default(k)] = self.default(v)
            return new_dict

        return obj


class JsonUtil:
    """
    Provides utility methods for dealing with JSON / Dict.
    """

    @staticmethod
    def read_jsonl_file(file_path: str, as_uncased_dict: bool = False) -> Union[Dict, UncasedDict]:
        """
        Reads JSON from file at path.
        :param file_path: Path to JSON file.
        :param as_uncased_dict: Whether to convert output to uncased dict
        :return: Dictionary content of file.
        """
        content = {}
        with open(file_path) as file:
            lines = file.readlines()
        for line in lines:
            json_dict = json.loads(line)
            for key, val in json_dict.items():
                if key not in content:
                    content[key] = []
                content[key].append(val)
        return UncasedDict(content) if as_uncased_dict else content

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
    def save_to_json_file(dict_: Dict, filepath: str) -> None:
        """
        Converts the dictionary to json
        :param dict_: the dictionary to save as json
        :param filepath: The path to save the json to
        :return: None
        """
        with open(filepath, 'w') as f:
            json.dump(dict_, f, indent=4, cls=NpEncoder)

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
            if param in source:
                entry[param] = source[param]
        return entry

    @staticmethod
    def as_dict(obj: Any) -> Dict:
        """
        Converts object to dictionary using the np encoder.
        :param obj: The object to encode and decode as json
        :return: The dictionary of the object.
        """
        obj_str = json.dumps(obj, cls=NpEncoder)
        return json.loads(obj_str)

    @staticmethod
    def get_all_fields(obj: Any) -> List:
        """
        Gets the name of all fields (keys) in the obj.
        :param obj: Python representation of the json.
        :return: A list of all attribute in the obj.
        """

        def add_child_fields():
            """
            Adds the children fields to the central list.
            """
            child_ordered_fields = JsonUtil.get_all_fields(v)
            ordered_fields.extend([c for c in child_ordered_fields if c not in fields])
            fields.update(set(child_ordered_fields))

        ordered_fields = []
        fields = set()
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k not in fields:
                    fields.add(k)
                    ordered_fields.append(k)
                add_child_fields()
        elif isinstance(obj, list):
            for v in obj:
                add_child_fields()
        return ordered_fields
