from enum import Enum, EnumMeta
from typing import Any, Dict

import collections
from yaml.nodes import Node, MappingNode
from yaml.constructor import ConstructorError
from yaml.loader import SafeLoader

from tgen.common.util.file_util import FileUtil
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.constants.deliminator_constants import COLON
from tqdm import tqdm


class CustomLoader(SafeLoader):
    __top_level_reached = False

    def construct_custom(self, _, node: Node) -> Any:
        """
        Constructs (mostly) any object that is not known to the yaml parser already
        :param _: unused, left for api
        :param node: The yaml node being parsed
        :return: The created object
        """
        class_path = node.tag.split(COLON)[-1]
        cls = ReflectionUtil.get_cls_from_path(class_path)
        if type(cls).__name__ in ["function", "builtin_function_or_method"] or "builtins" in class_path:
            return cls
        if isinstance(cls, EnumMeta):
            return self._create_enum_from_meta(cls, node)
        data = cls.__new__(cls)

        if hasattr(data, '__setstate__'):
            state = self.construct_mapping(node, deep=True)
            data.__setstate__(state)
        else:
            state = self.construct_mapping(node)
            data.__dict__.update(state)
        return data

    def _create_enum_from_meta(self, enum_meta: EnumMeta, node: Node) -> Enum:
        """
        Creates an enum from its meta obj
        :param enum_meta: The meta obj for an enum
        :param node: The yaml node containing the enum's value
        :return: The enum with the value contained in the node
        """
        value = self.construct_object(node.value[0])
        find_enum = [e for e in enum_meta if e.value == value]
        if len(find_enum) > 0:
            return find_enum.pop()

    def construct_object(self, node, deep=False) -> Any:
        """
        Overrides the normal yaml loader to make custom objects
        :param node: The node being parsed
        :param deep: Used in the yaml parser
        :return: The constructed object
        """
        if node.tag not in self.yaml_constructors:
            self.yaml_constructors[node.tag] = self.construct_custom
        return super().construct_object(node, deep)

    def construct_mapping(self, node, deep=False):
        """
        Overwritten to allow tqdm on top level
        :param node: Yaml Node
        :param deep: from yaml API
        :return: The constructed mapping
        """
        if not self.__top_level_reached:
            return self._run_top_level(node, deep)
        return super().construct_mapping(node, deep)

    def _run_top_level(self, node, deep=False) -> Dict:
        """
        Copied from BaseConstructor to allow tqdm
        :param node: Yaml Node
        :param deep: from yaml API
        :return: The constructed mapping for top level
        """
        self.__top_level_reached = True
        if isinstance(node, MappingNode):
            self.flatten_mapping(node)
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None,
                                   "expected a mapping node, but found %s" % node.id,
                                   node.start_mark)
        mapping = {}
        for key_node, value_node in tqdm(node.value, desc="Loading objects from yaml"):
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, collections.abc.Hashable):
                raise ConstructorError("while constructing a mapping", node.start_mark,
                                       "found unhashable key", key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


class YamlUtil:

    @staticmethod
    def read(path2yaml: str) -> Dict:
        """
        Reads a yaml file into a python obj
        :param path2yaml: The path to the yaml file
        :return: The file as a python obj
        """
        return FileUtil.read_yaml(path2yaml, loader=CustomLoader)

    @staticmethod
    def write(content: Dict, output_path: str) -> None:
        """
        Writes the yaml file
        :param content: The content as a python obj
        :param output_path: The path to save to
        :return: None
        """
        FileUtil.write_yaml(content, output_path)
