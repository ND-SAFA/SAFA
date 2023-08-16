from enum import Enum, EnumMeta
from typing import Dict

from ruamel.yaml.nodes import Node
from yaml.loader import SafeLoader

from tgen.common.util.file_util import FileUtil
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.constants.deliminator_constants import COLON


class CustomLoader(SafeLoader):

    def construct_custom(self, loader, node):
        class_path = node.tag.split(COLON)[-1]
        cls = ReflectionUtil.get_cls_from_path(class_path)
        if type(cls).__name__ == "function":
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

    def construct_object(self, node, deep=False):
        if node.tag not in self.yaml_constructors:
            self.yaml_constructors[node.tag] = self.construct_custom
        return super().construct_object(node, deep)


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
